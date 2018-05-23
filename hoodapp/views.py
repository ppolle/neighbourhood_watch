from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,CreateHoodForm

# Create your views here.
def index(request):
	'''
	This view class will render the index  landing page
	'''
	return render(request,'index.html')

def signup(request):
	'''
	This view class will implement user signup
	'''
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignUpForm()
	return render(request, 'authentication/signup.html', {'form': form})

def createHood(request):
	'''
	This view class will create an instance of a neighbourhood
	'''
	if request.method == 'POST':
		form = CreateHoodForm(request.POST)
		if form.is_valid():
			hood = form.save(commit = False)
			hood.save()
			return redirect('index')

	else:
		form = CreateHoodForm()
	return render(request,'hood/create.html',{"form":form})


