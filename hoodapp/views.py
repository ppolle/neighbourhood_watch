from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,CreateHoodForm,CreateBusinessForm
from .models import Neighbourhood,Business,Profile

# Create your views here.
def index(request):
	'''
	This view function will render the index  landing page
	'''
	neighbourhoods = Neighbourhood.objects.all()
	return render(request,'index.html',{"neighbourhoods":neighbourhoods})

def signup(request):
	'''
	This view function will implement user signup
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
	This view function will create an instance of a neighbourhood
	'''
	if request.method == 'POST':
		form = CreateHoodForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')

	else:
		form = CreateHoodForm()
	return render(request,'hood/create.html',{"form":form})

def editHood(request,hood_id):
	'''
	This view function will edit an instance of a neighbourhood
	'''
	
	if request.method == 'POST':
		form = CreateHoodForm(request.POST,instance = Neighbourhood.objects.get(pk = hood_id))
		if form.is_valid():
			form.save()
			
			return redirect('index')
	else:
		form = CreateHoodForm(instance = Neighbourhood.objects.get(pk = hood_id))

	return render(request,'hood/edit.html',{"form":form})


def createBusiness(request):
	'''
	This function will create a Business Instance
	'''
	if request.method == 'POST':
		form = CreateBusinessForm(request.POST)
		if form.is_valid():
			business = form.save(commit = False)
			business.save()
			return redirect('index')
	else:
		form = CreateBusinessForm()
	return render(request,'business/create.html',{"form":form})

def businessIndex(request):
	'''
	This post will fetch all business instances belonging to the current logged in user
	'''
	businesses= Business.objects.all()
	return render(request,'business/index.html',{"businesses":businesses})

def profile(request):
	'''
	This view function will fetch a user's profile
	'''
	profile = Profile.objects.get(user = request.user)
	return render(request,'accounts/profile.html',{"profile":profile})