"""
eox_theming URL Configuration
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('eox_theming.management.urls', namespace='eox-theming-management')),
]
