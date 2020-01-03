# -*- coding: utf-8 -*-
"""
Tests for the custom template tags
"""
import glob, os
import json

from django.test import TestCase
from django.test.utils import override_settings
from parameterized import parameterized

from eox_theming import configuration


def get_all_test_cases():
    """
    Finds all the files in the same directory as this that end in .txt
    """
    results = []
    for pathname in glob.glob('{}/*.txt'.format(os.path.dirname(os.path.abspath(__file__)))):
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
            case_result = eval(code, my_globals)

        # For now we compare the results as being the same without
        # trailing and leading spaces
        self.assertEqual(case_result, ''.join(output.splitlines()))


    @parameterized.expand(get_all_test_cases)
    def test_case(self, name, pathname):
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
