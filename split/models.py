# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Expense(models.Model):
	class Meta:
		app_label = 'split'

	name = models.CharField(max_length=255)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_by = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	group = models.CharField(max_length=255)

class SplitExpense(models.Model):
	class Meta:
		app_label = 'split'
	user = models.CharField(max_length=255, db_index=True)
	paid = models.DecimalField(max_digits=10, decimal_places=2)
	owes = models.DecimalField(max_digits=10, decimal_places=2)
	txn = models.ForeignKey('Expense')
