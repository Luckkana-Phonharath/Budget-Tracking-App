from django.contrib import admin
from .models import BudgetCategory, Budget, Transaction



# Register your models here.
admin.site.register(BudgetCategory)
admin.site.register(Budget)
admin.site.register(Transaction)
