from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Catalogue
from .forms import CatalogueForm
from django.core.files.uploadedfile import SimpleUploadedFile

class CatalogueModelTest(TestCase):
    def setUp(self):
        # Create a sample Catalogue for testing
        self.catalogue = Catalogue.objects.create(
            title="Test PDF",
            pdf=SimpleUploadedFile("test.pdf", b"%PDF-1.4\n", content_type="application/pdf")
        )

    def test_str_method(self):
        # Test the __str__ method returns the title
        self.assertEqual(str(self.catalogue), "Test PDF")

    def test_uploaded_at_auto_set(self):
        # Test timestamp is auto-set
        self.assertIsNotNone(self.catalogue.uploaded_at)

class CatalogueFormTest(TestCase):
    def test_form_valid(self):
        # Test form with valid data
        pdf_file = SimpleUploadedFile("test.pdf", b"%PDF-1.4\n", content_type="application/pdf")
        form = CatalogueForm(data={'title': 'Valid Title'}, files={'pdf': pdf_file})
        self.assertTrue(form.is_valid())

    def test_title_required(self):
        # Test form fails without title
        form = CatalogueForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class CatalogueViewTest(TestCase):
    def setUp(self):
        # Setup test client and users
        self.client = self.client  # Django's test HTTP client
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.smart_group = Group.objects.create(name='SmartUser')
        self.user.groups.add(self.smart_group)
        self.client.login(username='testuser', password='pass')  # Login as SmartUser

    def test_home_view_authenticated_smartuser(self):
        # Test home shows upload link for SmartUser
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload New Catalogue')

    def test_upload_view_permission_denied(self):
        # Test upload redirects normal user
        normal_user = User.objects.create_user(username='normal', password='pass')
        self.client.login(username='normal', password='pass')
        response = self.client.get(reverse('upload_catalogue'))
        self.assertRedirects(response, reverse('catalogue_list'))

    def test_catalogue_list_renders(self):
        # Test list view shows a catalogue
        Catalogue.objects.create(title="Sample", pdf=SimpleUploadedFile("sample.pdf", b"%PDF-1.4\n", content_type="application/pdf"))
        response = self.client.get(reverse('catalogue_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample")