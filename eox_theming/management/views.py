# -*- coding: utf-8 -*-
"""
The views for the plugin management
"""

from __future__ import unicode_literals

import json
from os.path import dirname, realpath
from subprocess import CalledProcessError, check_output

from django.http import HttpResponse
from django.utils import six

import eox_theming


def info_view(request):  # pylint: disable=unused-argument
    """
    Basic view to show the working version and the exact git commit of the
    installed app
    """
    try:
        working_dir = dirname(realpath(__file__))
        git_data = six.text_type(check_output(
            ["git", "rev-parse", "HEAD"], cwd=working_dir))
    except CalledProcessError:
        git_data = ""

    response_data = {
        "version": eox_theming.__version__,
        "name": "eox-theming",
        "git": git_data.rstrip('\r\n'),
    }
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
