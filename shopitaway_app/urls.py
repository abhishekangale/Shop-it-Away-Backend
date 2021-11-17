from re import template
from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ShopItAway APIs",
        default_version='v1',
        description="Backend API endpoint for Shop-it-Away Project.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user/register/', views.register),
    path('user/login/', views.login),
    path('user/items', views.item),
    path('user/itemcount',views.itemcount),
    path('user/postitem',views.postitem),
    path('user/updateitem',views.updateitem),
    path('user/deleteitem',views.deleteitem),
    path('user/assignotp',views.assignOTP),
    path('user/verifyotp',views.verifyOTP)
]