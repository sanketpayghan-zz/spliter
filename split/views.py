# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from .models import Expense, SplitExpense
from .utils import decimal_default
from django.db.models import Sum
from django.db import transaction
import json
from decimal import Decimal


# Create your views here.

class ExpenseView(View):
	def __init__(self):
		self.response = {'message': 'Expense added successfully.'}

	def post(self, request):
		"""
		Data has following format:
		name - Transaction name
		amount - Transasction amount
		paid - {'user1': amount1, 'user2': amount2}
		owes = {'user1': amount1, 'user3': amonut2}
		"""
		try:
			data = request.POST
			total_paid, total_owes = 0, 0
			splits = []
			paid = json.loads(data.get('paid', "{}"))
			owes = json.loads(data.get('owes', "{}"))
			for user, amount in paid.iteritems():
				total_paid = total_paid + Decimal(amount)
			for user, amount in owes.iteritems():
				total_owes = total_owes + Decimal(amount)
			if Decimal(total_paid) != Decimal(data.get('amount')):
				self.response['message'] = "total amount paid does not match with transaction amount."
				return HttpResponseBadRequest(json.dumps(self.response), content_type='application/json')
			if total_owes != Decimal(data.get('amount')):
				self.response['message'] = "total owned amount does not match with transaction amount."
				return HttpResponseBadRequest(json.dumps(self.response), content_type='application/json')
			with transaction.atomic():
				expense = Expense.objects.create(name=data.get('name'),
					amount = data.get('amount'), created_by = data.get('created_by'), group=data['group'])
				for user, amount in paid.iteritems():
					splits.append(SplitExpense(user=user,paid=amount,owes=owes.get(user, 0), txn=expense))
					if user in owes:
						owes.pop(user)
				for user, amount in owes.iteritems():
					splits.append(SplitExpense(user=user,paid=0,owes=amount, txn=expense))
				SplitExpense.objects.bulk_create(splits)
			return HttpResponse(json.dumps(self.response), content_type='application/json')
		except KeyError as e:
			self.response['message'] = 'Mandatory input parameter missing.'
			return HttpResponseBadRequest(json.dumps(self.response), content_type='application/json')

	def get(self, request):
		try:
			group = request.GET['group']
			result = SplitExpense.objects.filter(txn__group=group).values('user').annotate(paid_sum=Sum('paid') - Sum('owes')).order_by('paid_sum')
			simplified = []
			i, j = 0, len(result) - 1
			while i < j:
				transaction = {}
				transaction['from'] = result[i]['user']
				transaction['to'] = result[j]['user']
				if abs(result[i]['paid_sum']) >= abs(result[j]['paid_sum']):
					transaction['amount'] = abs(result[j]['paid_sum'])
					result[i]['paid_sum'] = result[i]['paid_sum'] + result[j]['paid_sum']
					j = j - 1
				else:
					transaction['amount'] = abs(result[i]['paid_sum'])
					result[j]['paid_sum'] = result[i]['paid_sum'] + result[j]['paid_sum']
					i = i + 1
				if transaction['amount'] > 0:
					simplified.append(transaction)
			self.response = {'message': 'Simplified expenses.'}
			self.response['simplified'] = simplified
			return HttpResponse(json.dumps(self.response, default=decimal_default), content_type='application/json')
		except KeyError as e:
			self.response['message'] = 'Mandatory input parameter missing.'
			return HttpResponseBadRequest(json.dumps(self.response), content_type='application/json')




