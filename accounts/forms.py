from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contractor,labour,Profile

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','contact', 'gender', 'address','city','state','pincode')
