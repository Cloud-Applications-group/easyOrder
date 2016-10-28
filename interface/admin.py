from django.contrib import admin
from .models import Restaurant

# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'rating', 'info']
    list_display_links = ['user']



admin.site.register(Restaurant, RestaurantAdmin)