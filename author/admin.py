from django.contrib import admin

from .models import Author
from unfold.admin import ModelAdmin

@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('user',  'city', 'state', 'country')
    list_filter = ('city', 'state', 'country')
    search_fields = ('city', 'state', 'country')
    
