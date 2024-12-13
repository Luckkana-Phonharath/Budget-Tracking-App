from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Friendship (models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username} ({self.status})'

class Message (models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


