"""
eox_theming management urls
"""
from django.conf.urls import url

from eox_theming.management import views

urlpatterns = [
    url(r'^eox-info$', views.info_view),
]
