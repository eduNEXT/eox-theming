# -*- coding: utf-8 -*-
"""
Tests for the custom template tags
"""
from django.test import TestCase
from django.template import Context, Template
from mock import patch
import json



class TestsUseCases(TestCase):

    def run_case(self, data, code, output):
        clean_data = ''.join(data.splitlines())
        case_data = json.loads(clean_data)

        case_result = eval(code)

        print('======')
        print(case_result)
        print('======')
        print(''.join(output.splitlines()))  # si es esto?
        print('======')


    def test_all(self):

        f = open('eox_theming/tests/api_v1/case_001.txt', 'r')
        text = f.read()
        blocks = text.split("======")

        test_case = {}
        for idx, block in enumerate(blocks):
            key = block.lower().strip(' ')
            if key in ['data', 'code', 'output']:
                test_case[key] = blocks[idx + 1]

        self.run_case(**test_case)

        self.fail()
