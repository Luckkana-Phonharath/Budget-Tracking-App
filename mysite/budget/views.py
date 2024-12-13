
from django.shortcuts import render, redirect
from .models import Transaction, BudgetCategory, Budget
from social.models import Friendship, Message
from .forms import TransactionForm, BudgetCategoryForm, BudgetAllocationForm, BudgetForm
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from users.models import Profile
from django.db.models import Sum, Q
from django.utils import timezone
import pdfkit
import io



# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

#Budget Category
@login_required
def category(request):
    if request.user.is_authenticated:
        categories = BudgetCategory.objects.filter(user=request.user)  # Filter by logged-in user
    else:
        categories = None
    return render(request, 'budgetCategory/category_index.html', {'categories': categories})

@login_required
def add_category(request):
    form = BudgetCategoryForm(request.POST or None)

    if form.is_valid():
        budget_category = form.save(commit=False)
        budget_category.user = request.user
        budget_category.save()

        return redirect('category')

    return render(request, 'budgetCategory/category_form.html', {'form': form})

@login_required
def update_category(request, id):
    category = BudgetCategory.objects.get(id=id)
    form = BudgetCategoryForm(request.POST or None, instance=category)

    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('allocate_budget')
    else:
        form = BudgetCategoryForm(instance=category)

    return render(request, 'budgetCategory/edit_category.html', {'form': form})

@login_required
def delete_category(request, id):
    category = BudgetCategory.objects.get(id=id)

    if request.method == 'POST':
        category.delete()
        return redirect('category')
    return render(request, 'budgetCategory/category_delete.html', {'category': category})

#Budget
@login_required
def budget(request):
    budgets = Budget.objects.all()
    context = {'budgets': budgets}
    return render(request, 'budget.html', context)

@login_required
def update_budget(request, id):
    budget = Budget.objects.get(id=id, user=request.user)
    form = BudgetForm(request.POST or None, instance=budget)

    if request.method == 'POST' and form.is_valid():
        if not form.cleaned_data['category']:
            form.cleaned_data['category'] = BudgetCategory.objects.first()

        form.save()
        return redirect('allocate_budget')

    return render(request, 'budget/update_budget.html', {'form': form, 'budget': budget})



#Transaction
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully.")
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user, instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})


@login_required
def allocate_budget(request):
    profile = Profile.objects.get(user=request.user)
    monthly_income = profile.monthly_income
    categories = BudgetCategory.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    if request.method == 'POST':
        form = BudgetAllocationForm(user=request.user, data=request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']


            if amount > monthly_income:
                messages.error(request, "Amount exceeds available monthly income!")
            else:

                profile.monthly_income -= amount
                profile.save()


                budget, created = Budget.objects.get_or_create(user=request.user, category=category)
                budget.amount += amount
                budget.save()

            return redirect('allocate_budget')

    else:
        form = BudgetAllocationForm(user=request.user)

    context = {
        'form': form,
        'monthly_income': monthly_income,
        'budgets': budgets,
    }

    return render(request, 'budget/allocate_budget.html', context)

@login_required()
def dashboard(request):
    messages = Message.objects.filter(receiver=request.user)
    friend_requests = Friendship.objects.filter(receiver=request.user, status='pending')
    budgets = Budget.objects.filter(user=request.user)
    data = []

    for budget in budgets:

        category_name = budget.category.name if budget.category else 'Uncategorized'
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category
        ).aggregate(total=Sum('amount'))['total'] or 0
        remaining = budget.amount - spent
        progress = (spent / budget.amount * 100) if budget.amount > 0 else 0

        data.append({
            'category': category_name,
            'amount': budget.amount,
            'spent': round(spent, 2),
            'remaining': round(remaining, 2),
            'progress': round(progress, 2)
        })

    return render(request, 'dashboard.html', {
        'data': data,
        'messages': messages,
        'friend_requests': friend_requests
    })


@login_required
def report_view(request):
    # Get the current date and the first day of the current month
    now = timezone.now()
    first_of_month = now.replace(day=1)


    budgets = Budget.objects.filter(user=request.user, created_at__gte=first_of_month)


    budget_data = []
    for budget in budgets:
        spent = \
        Transaction.objects.filter(user=request.user, category=budget.category, date__gte=first_of_month).aggregate(
            Sum('amount'))['amount__sum'] or 0
        ratio = (spent / budget.amount * 100) if budget.amount else 0
        budget_data.append({
            'category': budget.category.name if budget.category else 'Uncategorized',
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': budget.amount - spent,
            'ratio': ratio
        })


    transactions = Transaction.objects.filter(user=request.user, date__gte=first_of_month)


    friend_requests = Friendship.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        created_at__gte=first_of_month
    )


    messages_received = Message.objects.filter(receiver=request.user, created_at__gte=first_of_month)

    context = {
        'budget_data': budget_data,
        'transactions': transactions,
        'friend_requests': friend_requests,
        'messages_received': messages_received
    }

    return render(request, 'report/report.html', context)


@login_required
def report_view_cv(request):


    now = timezone.now()
    first_of_month = now.replace(day=1)


    budgets = Budget.objects.filter(user=request.user, created_at__gte=first_of_month)


    budget_data = []
    for budget in budgets:
        spent = \
        Transaction.objects.filter(user=request.user, category=budget.category, date__gte=first_of_month).aggregate(
            Sum('amount'))['amount__sum'] or 0
        ratio = (spent / budget.amount * 100) if budget.amount else 0
        category_name = budget.category.name if budget.category else 'Uncategorized'
        budget_data.append({
            'category': category_name,
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': budget.amount - spent,
            'ratio': ratio
        })


    transactions = Transaction.objects.filter(user=request.user, date__gte=first_of_month)


    friend_requests = Friendship.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        created_at__gte=first_of_month
    )


    messages_received = Message.objects.filter(receiver=request.user, created_at__gte=first_of_month)

    context = {
        'budget_data': budget_data,
        'transactions': transactions,
        'friend_requests': friend_requests,
        'messages_received': messages_received
    }

    template = loader.get_template('report/report.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = 'monthly-budget.pdf'

    return response




