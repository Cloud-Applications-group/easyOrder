from django.conf.urls import url, include
from interface import views

from interface.api import OrderResource

order_resource = OrderResource()

urlpatterns = (
    url(r'^$', views.login, name='login'),
    url(r'home', views.homepage, name='home'),
    url(r'^api/', include(order_resource.urls))
)
