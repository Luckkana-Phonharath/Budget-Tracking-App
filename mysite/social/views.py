from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Friendship, Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


# Create your views here.
@login_required
def search_user(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
        return redirect('profile', username=user.username)
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)

@login_required
def send_friend_request(request, username):
    sender = request.user
    receiver = get_object_or_404(User, username=username)


    if sender == receiver:
        return redirect('profile', username=username)


    existing_request = Friendship.objects.filter(sender=sender, receiver=receiver)
    if not existing_request:

        Friendship.objects.create(sender=sender, receiver=receiver)

    return redirect('profile', username=username)

@login_required
def accept_friend_request(request, username):
    receiver = request.user
    sender = get_object_or_404(User, username=username)


    friendship = get_object_or_404(Friendship, sender=sender, receiver=receiver, status='pending')


    friendship.status = 'accepted'
    friendship.save()

    return redirect('profile', username=username)


@login_required
def reject_friend_request(request, username):
    receiver = request.user
    sender = get_object_or_404(User, username=username)


    friendship = get_object_or_404(Friendship, sender=sender, receiver=receiver, status='pending')


    friendship.status = 'rejected'
    friendship.save()

    return redirect('profile', username=username)

@login_required
def send_message(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, f'Message sent to {message.receiver.username}!')
            return redirect('send_message')
        else:
            messages.error(request, 'There was an error sending your message. Please try again.')
    else:
        accepted_friends = Friendship.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)),
            status='accepted'
        ).values_list('sender', 'receiver')

        accepted_user_ids = {user_id for pair in accepted_friends for user_id in pair if user_id != request.user.id}
        form = MessageForm()
        form.fields['receiver'].queryset = User.objects.filter(id__in=accepted_user_ids)

    return render(request, 'send_message.html', {'form': form})

def mark_message_read(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id, receiver=request.user)
        message.is_read = not message.is_read
        message.save()
    return redirect('dashboard')