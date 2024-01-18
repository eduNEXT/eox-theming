"""
eox_theming URL Configuration
"""
from django.urls import include, re_path

urlpatterns = [
    re_path(r'', include(('eox_theming.management.urls', 'eox_theming'), namespace='eox-theming-management')),
]
