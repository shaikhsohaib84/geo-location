from django.urls import re_path
from .views import  getAddressDetails

urlpatterns = [
    re_path(r'^get-address-details/', getAddressDetails)
]