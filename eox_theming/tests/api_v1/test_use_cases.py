# -*- coding: utf-8 -*-
"""
Tests for the custom template tags
"""
from django.test import TestCase
from django.template import Context, Template
from parameterized import parameterized
from mock import patch
import json


def get_all_test_cases():
    return [
        'case_001.txt',
    ]


class TestsUseCasesSequence(TestCase):

    def run_case(self, data, code, output):
        clean_data = ''.join(data.splitlines())
        case_data = json.loads(clean_data)

        case_result = eval(code)

        # print('======')
        # print(case_result)
        # print('======')
        # print(''.join(output.splitlines()))  # si es esto?
        # print('======')

        self.assertEqual(case_result, ''.join(output.splitlines()))


    @parameterized.expand(get_all_test_cases)
    def test_case(self, name):

        f = open('eox_theming/tests/api_v1/{}'.format(name), 'r')
        text = f.read()
        blocks = text.split("======")

        test_case = {}
        for idx, block in enumerate(blocks):
            key = block.lower().strip(' ')
            if key in ['data', 'code', 'output']:
                test_case[key] = blocks[idx + 1]

        self.run_case(**test_case)

        # self.fail()
