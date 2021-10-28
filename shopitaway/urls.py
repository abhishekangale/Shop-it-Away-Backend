from django.urls import include, path
from rest_framework import routers
from shopitaway.shopitaway_app import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('shopitaway.shopitaway_app.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]