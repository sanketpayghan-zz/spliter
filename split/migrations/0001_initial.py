# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-27 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_by', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SplitExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(db_index=True, max_length=255)),
                ('paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('txn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Split.Expense')),
            ],
        ),
    ]