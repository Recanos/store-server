from django.urls import include, path
from rest_framework import routers

from api.views import BasketModelViewset, ProductModelViewset

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewset)
router.register(r'baskets', BasketModelViewset)
urlpatterns = [
    path('', include(router.urls)),

]