# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Expense
# Create your tests here.

class ExpenseTestCase(TestCase):
    def setup(self):
        pass

    def test_check(self):
        self.assertEqual('Same', 'Same')
