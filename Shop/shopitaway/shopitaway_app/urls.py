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
        description="Welcome to the world of coding",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]