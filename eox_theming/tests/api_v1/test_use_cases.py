# -*- coding: utf-8 -*-
"""
Tests for the custom template tags
"""
import glob
import json
import os
from functools import partial
from mock import patch, MagicMock

from django.test import TestCase
from django.test.utils import override_settings
from parameterized import parameterized

from eox_theming.test_utils import process_multiline_string
from eox_theming import configuration
from eox_theming.api.v1.api import ThemingOptions


def get_all_test_cases(expr=None):
    """
    Finds all the files in the same directory as this that end in .txt
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if expr is None:
        expr = '*.txt'

    results = []
    for pathname in glob.glob('{}/{}'.format(base_dir, expr)):
        name = pathname.split('/')[-1].split('.')[0]
        results.append((name, pathname))

    return results


class TestsUseCasesSequence(TestCase):
    """
    Execute all the tests cases in a dynamic test definition
    """

    def run_case(self, data, code, output):
        """
        Run the case as defined in the text file
        """
        clean_data = ''.join(data.splitlines())
        case_data = json.loads(clean_data)

        my_globals = {
            'theming': configuration.ThemingConfiguration()
        }

        with override_settings(THEME_OPTIONS=case_data):
            case_result = eval(code, my_globals)  # pylint: disable=eval-used

        # For now we compare the results as being the same without
        # trailing and leading spaces
        self.assertEqual(
            process_multiline_string(case_result),
            process_multiline_string(output)
        )

    @parameterized.expand(get_all_test_cases)
    def test_case(self, name, pathname):  # pylint: disable=unused-argument
        """
        Dynamic test definition to run every case in this directory.

        The tests definitions must be files with the .txt extension,
        which must have 3 sections, one for the data to be loaded in
        the configuration, one for the lines that exemplify the code
        execution and one for the html or string results.
        """

        f = open(pathname, 'r')
        text = f.read()
        blocks = text.split("======")

        test_case = {}
        for idx, block in enumerate(blocks):
            key = block.lower().strip(' ')
            if key in ['data', 'code', 'output']:
                test_case[key] = blocks[idx + 1]

        self.run_case(**test_case)


class TestsUseCasesAPIV1Sequence(TestCase):
    """
    Execute all the tests cases from API V1 in a dynamic test definition
    """
    def run_case(self, defaults, data, code, output):
        """
        Run the case as defined in the text file
        """
        clean_defaults = ''.join(defaults.splitlines())
        case_defaults = json.loads(clean_defaults)

        clean_data = ''.join(data.splitlines())
        case_data = json.loads(clean_data)

        def_config = MagicMock(return_value=case_defaults)
        from_file = MagicMock(return_value=case_data)

        with patch.multiple(
            'eox_theming.api.v1.api.ThemingOptions',
            source_functions=[from_file],
            _get_default_configuration=def_config
        ):
            my_globals = {
                'theming': ThemingOptions()
            }

            case_result = eval(code, my_globals)  # pylint: disable=eval-used

            # For now we compare the results as being the same without
            # trailing and leading spaces
            self.assertEqual(
                process_multiline_string(case_result),
                process_multiline_string(output)
            )

    @parameterized.expand(partial(get_all_test_cases, expr='v1/*.txt'))
    def test_case(self, name, pathname):  # pylint: disable=unused-argument
        """
        Dynamic test definition to run every case in the directory v1/.

        The tests definitions must be files with the .txt extension,
        which must have 4 sections, one for the default configuration,
        one for the data to be loaded in the configuration, one for the
        lines that exemplify the code execution and one for the html
        or string results.
        """

        f = open(pathname, 'r')
        text = f.read()
        blocks = text.split("======")

        test_case = {}
        for idx, block in enumerate(blocks):
            key = block.lower().strip(' ')
            if key in ['defaults', 'data', 'code', 'output']:
                test_case[key] = blocks[idx + 1]

        self.run_case(**test_case)
