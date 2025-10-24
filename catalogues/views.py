from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Catalogue
from .forms import CatalogueForm

def home(request):
    catalogues = Catalogue.objects.all()
    is_smart_user = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            is_smart_user = True
        elif request.user.groups.filter(name='SmartUser').exists():
            is_smart_user = True

    return render(request, 'catalogues/home.html', {
        'catalogues': catalogues,
        'is_smart_user': is_smart_user,
    })

def catalogue_list(request):
     catalogues = Catalogue.objects.all()
     is_smart_user = False
     if request.user.is_authenticated:
         if request.user.is_superuser or request.user.groups.filter(name='SmartUser').exists():
             is_smart_user = True

     return render(request, 'catalogues/catalogue_list.html', {
         'catalogues': catalogues,
         'is_smart_user': is_smart_user,
     })

@login_required
def upload_catalogue(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='SmartUser').exists()):
        return redirect('catalogue_list')

    if request.method == 'POST':
        form = CatalogueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogue_list')
    else:
        form = CatalogueForm()

    return render(request, 'catalogues/upload_catalogue.html', {'form': form})
