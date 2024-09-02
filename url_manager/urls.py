from django.urls import path

from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("create", views.create_short_url, name="create_short_url"),
    path("s/<str:short_endpoint>", views.redirect_to_long_url, name="redirect_to_long_url"),
]