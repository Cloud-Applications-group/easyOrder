# myapp/api.py

from tastypie.resources import ModelResource
from interface.models import Order
from interface.models import Menu


class OrderResource(ModelResource):
    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'
