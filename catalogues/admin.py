
# Register your models here.
from django.contrib import admin
from .models import Catalogue

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_at")   # show these columns in admin

