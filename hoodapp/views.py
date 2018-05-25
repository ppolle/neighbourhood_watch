from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,CreateHoodForm,CreateBusinessForm,EditprofileForm
from .models import Neighbourhood,Business,Profile,Join

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
	neighbourhood = Neighbourhood.objects.get(pk = hood_id)
	if request.method == 'POST':
		form = CreateHoodForm(request.POST,instance = neighbourhood)
		if form.is_valid():
			form.save()
			
			return redirect('index')
	else:
		form = CreateHoodForm(instance = neighbourhood)

	return render(request,'hood/edit.html',{"form":form,"neighbourhood":neighbourhood})


def createBusiness(request):
	'''
	This function will create a Business Instance
	'''
	if request.method == 'POST':
		form = CreateBusinessForm(request.POST)
		if form.is_valid():
			business = form.save(commit = False)
			business.save()
			return redirect('allBusinesses')
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

def editProfile(request):
	'''
	This view function will edit a profile instance
	'''
	profile = Profile.objects.get(user = request.user)
	if request.method == 'POST':
		form = EditprofileForm(request.POST,instance = profile )
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = EditprofileForm(instance = profile )

	return render(request,'accounts/edit.html',{"form":form})

def editBusiness(request,businessId):
	'''
	This view function will edit an instance of a Business
	'''
	business = Business.objects.get(pk = businessId)
	if request.method == 'POST':
		form = CreateBusinessForm(request.POST,instance = business)
		if form.is_valid():
			form.save()
			return redirect('allBusinesses')
	else:
		form = CreateBusinessForm(instance = business)
	return render(request,'business/edit.html',{"form":form,"business":business})

def search(request):
	'''
	This view function will implement search of a hood
	'''
	if request.GET['search']:
		search_term = request.GET.get("search")
		hoods = Neighbourhood.objects.filter(name__icontains = search_term)
		message = f"{search_term}"

		return render(request,'hood/search.html',{"message":message,"hoods":hoods})
	else:
		message = "You Haven't searched for any item"
		return render(request,'hood/search.html',{"message":message})

def join(request,hoodId):
	'''
	This view function will implement adding 
	'''
	neighbourhood = Neighbourhood.objects.get(pk = hoodId)
	if Join.objects.filter(user_id = request.user).exists():
		
		Join.objects.filter(user_id = request.user).update(hood_id = neighbourhood)
	else:

		Join(user_id=request.user,hood_id = neighbourhood).save()

	return redirect('hoodHome',hoodId)

def hoodHome(request,hoodId):
	'''
	This functin will retrive instances of a neighbourhood
	'''
	hood = Neighbourhood.objects.get(pk = hoodId)
	return render(request,'hood/index.html',{"hood":hood})