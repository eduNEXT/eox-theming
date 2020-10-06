"""
eox_theming URL Configuration
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include(('eox_theming.management.urls', 'eox_theming'), namespace='eox-theming-management')),
]
