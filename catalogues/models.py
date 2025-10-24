from django.db import models

class Catalogue(models.Model):
    title = models.CharField(max_length=50)
    pdf = models.FileField(upload_to='catalogues_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
