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
    user = fields.ForeignKey(UserResource, 'user')

    def hydrate(self, bundle):
        request_method = bundle.request.META['REQUEST_METHOD']

        if request_method == 'POST':
            user = bundle.request.user
            is_available = bool(bundle.data.get('is_available'))
            keys = list(bundle.data.keys())
            restaurant = Restaurant.objects.all().filter(user=user)
            if restaurant:
                for i in keys:
                    restaurant.update(**{i : bundle.data.get(i)})

        return Exception("Updated")


    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'
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
    user = fields.ForeignKey(UserResource, 'user')
    restaurant = fields.ForeignKey(RestaurantResource, 'restaurant')

    def hydrate(self, bundle):
        request_method = bundle.request.META['REQUEST_METHOD']

        if request_method == 'POST':
            user = bundle.request.user
            restaurant=Restaurant.objects.all().filter(user=user)
            menu = Menu.objects.all().filter(user=user).filter(restaurant=restaurant)
            if menu:
                menu = bool(bundle.data.get('menu'))
                restaurant.update(content=menu)

        return Exception("Updated")


    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'
        authorization = Authorization()