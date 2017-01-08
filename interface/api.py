# myapp/api.py
from tastypie.resources import ModelResource, Resource
from interface.models import *
from tastypie.constants import ALL
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authorization import ReadOnlyAuthorization, Authorization






class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }

class RestaurantResource(ModelResource):


    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        filtering = {

            'location_id': ALL_WITH_RELATIONS,
            'name': ALL_WITH_RELATIONS
        }





class RestaurantOrderResource(ModelResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant', full=True)
    user = fields.ForeignKey(UserResource, 'user', full=True)

    def apply_filters(self, request, applicable_filters):

        user = request.user
        restaurent = Restaurant.objects.all().filter(user=user)
        if request.user.is_anonymous():
            return Order.objects.none()
        order = Order.objects.all().filter(restaurant=restaurent)
        return order


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'rest_order'
        limit = 0


class UserOrderResource(ModelResource):
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant', full=True)

    def apply_filters(self, request, applicable_filters):

        user = request.user
        if request.user.is_anonymous():
            return Order.objects.none()
        order = Order.objects.all().filter(user=user)
        return order


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'user_order'
        limit = 0


class UserRestaurantResource(ModelResource):

    def apply_filters(self, request, applicable_filters):

        user = request.user
        if request.user.is_anonymous():
            return Order.objects.none()
        rest = Restaurant.objects.all().filter(user=user)
        return rest


    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'user_restaurant'
        excludes = ['user']
        limit = 0

class MenuResource(ModelResource):

    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()


class OrderResource(ModelResource):

    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'
        allowed_methods = ['get', 'post', 'patch', 'put']
        authorization = Authorization()
