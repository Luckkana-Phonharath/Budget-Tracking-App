from django import forms
from .models import Message,Friendship



class FriendRequestForm(forms.Form):
    username = forms.CharField(max_length=150, label="Friend's Username")

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols':50}),
        }