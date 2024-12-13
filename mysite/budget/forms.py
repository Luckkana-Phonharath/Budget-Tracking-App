from django import forms
from .models import Budget, BudgetCategory, Transaction

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = BudgetCategory.objects.filter(user=self.instance.user)

class BudgetCategoryForm(forms.ModelForm):
    class Meta:
        model = BudgetCategory
        fields = ['name']



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'type', 'amount', 'description']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = BudgetCategory.objects.filter(user=user)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})


class BudgetAllocationForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=BudgetCategory.objects.none(),
        label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = BudgetCategory.objects.filter(user=user)