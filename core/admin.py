from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Carousel, GeneralData, Support, Country, State, City, Thana

@admin.register(Carousel)
class CarouselAdmin(ModelAdmin):
    list_display = ['title', 'title_bn', 'subtitle', 'subtitle_bn', 'image', 'link', 'is_advertise']
    list_editable = ['is_advertise']
    list_filter = ['is_advertise']
    search_fields = ['title', 'title_bn', 'subtitle', 'subtitle_bn']
    list_per_page = 10


@admin.register(GeneralData)
class GeneralDataAdmin(ModelAdmin):
    list_display = ['address', 'phone', 'email', 'facebook', 'twitter', 'instagram', 'youtube']
    list_per_page = 10


@admin.register(Support)
class SupportAdmin(ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message']
    list_per_page = 10

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ['name', 'code', 'flag']
    list_per_page = 10


@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ['name', 'country']
    list_per_page = 10


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['name', 'state']
    list_per_page = 10


@admin.register(Thana)
class ThanaAdmin(ModelAdmin):
    list_display = ['name', 'city'] 
    list_per_page = 10
