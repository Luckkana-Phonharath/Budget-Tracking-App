# Generated by Django 2.2 on 2024-12-11 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0009_remove_budget_monthly_income'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetcategory',
            name='monthly_income',
        ),
    ]
