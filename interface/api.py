# myapp/api.py

from django.shortcuts import get_object_or_404
from tastypie.resources import ModelResource, Resource
from interface.models import Order
from interface.models import Restaurant



class OrderResource(ModelResource):

    def apply_filters(self, request, applicable_filters):


        if request.user.is_anonymous():
            return Order.objects.none()
        order = Order.objects.all().filter(restaurant=request.user)
        return order


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'



class RestaurantResource(ModelResource):
    def apply_filters(self, request, applicable_filters):
        return Restaurant.objects.all()

    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'


