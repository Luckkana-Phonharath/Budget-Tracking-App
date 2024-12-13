from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BudgetCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budget_categories")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_category_per_user')
        ]


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),('income', 'Income'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} ({self.category.name})"