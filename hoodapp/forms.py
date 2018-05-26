from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Neighbourhood,Business,Profile,Posts,Comments


class SignUpForm(UserCreationForm):
	'''
	Model form class to create a sign up form
	'''
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CreateHoodForm(forms.ModelForm):
	'''
	Model form class to render a create neighbourhood form
	'''
	class Meta:
		model = Neighbourhood
		fields = ['name','location','population','description']

class CreateBusinessForm(forms.ModelForm):
	'''
	model form class to render a create business form
	'''
	class Meta:
		model = Business
		fields = ['name','email_address','description']

class EditprofileForm(forms.ModelForm):
	'''
	model form class to render a edit profil form
	'''
	class Meta:
		model = Profile
		fields = ['bio']

class ForumPostForm(forms.ModelForm):
	'''
	model form class to render a create forum post form
	'''
	class Meta:
		model = Posts
		fields = ['title','body']

class CommentForm(forms.ModelForm):
	'''
	model form class to render a creat comment form
	'''
	class Meta:
		model = Comments
		fields = ['comment']



