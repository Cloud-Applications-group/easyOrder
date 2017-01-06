from django.contrib import admin
from .models import Restaurant, Order
from django.core import urlresolvers
from django.contrib.auth.models import User

# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_link', 'name', 'location_id', 'info']
    list_display_links = ['pk']

    # Foreign key link
    def user_link(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.pk])
        return u'<a href="%s">%s</a>' % (link, obj.user.username)

    user_link.allow_tags = True


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_link', 'restaurant_link', 'content', 'amount', 'status']
    list_display_links = ['pk']

    # Foreign key link
    def user_link(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.pk])
        return u'<a href="%s">%s</a>' % (link, obj.user.username)

    # Foreign key link
    def restaurant_link(self, obj):
        link = urlresolvers.reverse("admin:interface_restaurant_change", args=[obj.restaurant.pk])
        return u'<a href="%s">%s</a>' % (link, obj.restaurant.name)

    user_link.allow_tags = True
    restaurant_link.allow_tags = True

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Order, OrderAdmin)