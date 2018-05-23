from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Neighbourhood,Business,Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CreateHoodForm(forms.ModelForm):
	class Meta:
		model = Neighbourhood
		fields = ['name','location','population','description']

class CreateBusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		fields = ['name','email_address','description']

