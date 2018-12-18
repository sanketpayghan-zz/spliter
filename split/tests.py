# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Expense
# Create your tests here.

class ExpenseTestCase(TestCase):
    def setUp(self):
        expense = Expense.objects.create(name='Expense Test', amount=27.08, created_by='sanket')

    def test_check(self):
        expense = Expense.objects.get(name='Expense Test')
        self.assertEqual(expense.name, 'Expense Test')
