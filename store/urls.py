
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from products.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('products/', include('products.urls', namespace = 'products')),
    path('users/', include('users.urls', namespace = 'users')),
    path('accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls', namespace ='orders')),
    path('api/', include('api.urls', namespace ='api')),
    path('api-token-auth/', obtain_auth_token),
]


if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
