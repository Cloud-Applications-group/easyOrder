# myapp/api.py

from interface.models import *

from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL, Resource


class OrderResource(ModelResource):

    def apply_filters(self, request, applicable_filters):

        print request.user
        if request.user.is_anonymous():
            return Order.objects.none()
        order = Order.objects.all().filter(user=request.user)
        return order


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'



class RestaurantResource(ModelResource):
    def apply_filters(self, request, applicable_filters):
        id = request.GET.get('shop_id', None)
        if id:
            return Restaurant.objects.all().filter(shop_id=id)
        return Restaurant.objects.none()

    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'
        filtering = {
            'shop_id': ALL
        }



class MenuResource(ModelResource):
    def apply_filters(self, request, applicable_filters):
        return Menu.objects.all()

    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'
        filtering = {'restaurant': ALL}
