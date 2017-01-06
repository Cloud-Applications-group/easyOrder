# myapp/api.py
from tastypie.resources import ModelResource, Resource
from interface.models import *
from tastypie.constants import ALL
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields




class OrderResource(ModelResource):

    def apply_filters(self, request, applicable_filters):

        user = request.user
        restaurent = Restaurant.objects.all().filter(user=user)
        if request.user.is_anonymous():
            return Order.objects.none()
        order = Order.objects.all().filter(restaurant=restaurent)
        return order


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'



class RestaurantResource(ModelResource):
    # eg http://localhost:8000/api/v1/restaurant/?format=json
    # or
    # http://localhost:8000/api/v1/restaurant/?format=json&name__contains=test


    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'
        filtering = {

            'location_id': ALL_WITH_RELATIONS,
            'name': ALL_WITH_RELATIONS
        }



class MenuResource(ModelResource):
    # eg http://localhost:8000/api/v1/menu/?format=json&restaurant__name__contains=test
    restaurant = fields.ToOneField(RestaurantResource, 'restaurant', full=True)
    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'
        filtering = {
           'restaurant': ALL_WITH_RELATIONS
        }