from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from budget.models import BudgetCategory
from django.contrib.auth.models import User
from .models import Profile
from social.models import Friendship
from PIL import Image
from django.db.models import Q

DEFAULT_CATEGORIES = ['Gas', 'Food', 'Entertainment', 'Rent', 'Utilities']

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # login in user to continue asking budget questions.
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}!')
            return redirect('create_profile')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Attach the logged-in user
            profile.save()

            for category in DEFAULT_CATEGORIES:
                if not BudgetCategory.objects.filter(user=request.user, name=category).exists():
                    BudgetCategory.objects.create(user=request.user, name=category)

            messages.success(request, 'Profile created successfully!')
            return redirect('category')
    else:
        form = ProfileUpdateForm()

    return render(request, 'users/profile_form.html', {'form': form})



@login_required
def profile_view(request, username):
    # Fetch the profile of the user being viewed
    viewed_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=viewed_user)

    # Fetch logged-in user's friendships
    user_friends = Friendship.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)),
        status='accepted'
    ).values_list('sender', 'receiver')

    # Prepare friend list for logged-in user's profile
    friends = User.objects.filter(id__in={u for pair in user_friends for u in pair if u != request.user.id})

    # Check friendship status for "Send Friend Request" button
    friendship_status = None
    if viewed_user != request.user:
        friendship = Friendship.objects.filter(
            Q(sender=request.user, receiver=viewed_user) |
            Q(sender=viewed_user, receiver=request.user)
        ).first()
        friendship_status = friendship.status if friendship else None

    # Determine if we are viewing the logged-in user's profile
    is_own_profile = request.user == viewed_user

    context = {
        'viewed_user': viewed_user,
        'profile': profile,
        'friends': friends if is_own_profile else None,
        'is_own_profile': is_own_profile,
        'friendship_status': friendship_status,
    }

    return render(request, 'users/profile.html', context)






