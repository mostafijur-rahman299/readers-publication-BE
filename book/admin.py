from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Book, Category

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        'title', 'title_bn', 'status', 'is_available', 'is_new_arrival', 'is_favorite', 'is_comming_soon', 'is_best_seller',
        'sku', 'isbn', 'price', 'discounted_price', 'available_copies'
    )
    list_filter = ('status', 'is_available', 'is_new_arrival', 'is_favorite', 'is_comming_soon', 'is_best_seller')
    list_editable = ('status', 'is_available', 'is_new_arrival', 'is_favorite', 'is_comming_soon', 'is_best_seller')
    list_per_page = 10
    list_max_show_all = 100
    search_fields = ('title', 'title_bn', 'sku', 'isbn', 'publisher', 'translator', 'edition', 'language', 'dimensions', 'weight', 'country')
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_bn', 'slug', 'index_number', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active', 'index_number')
    search_fields = ('name', 'name_bn', 'slug')
    ordering = ('index_number',)
    list_filter = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}   

