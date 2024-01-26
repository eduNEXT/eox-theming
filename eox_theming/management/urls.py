"""
eox_theming management urls
"""
from django.urls import re_path

from eox_theming.management import views

urlpatterns = [
    re_path(r'^eox-info$', views.info_view),
]
