from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'biography', 'location', 'monthly_income')
        widgets = {
            'biography': forms.Textarea(attrs={'placeholder': 'Tell us about yourself', 'rows': 5}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter your location'}),
            'monthly_income': forms.NumberInput(attrs={'placeholder': 'Enter your monthly income'}),
        }



