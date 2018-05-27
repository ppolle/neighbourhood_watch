from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,CreateHoodForm,CreateBusinessForm,EditprofileForm,ForumPostForm,CommentForm
from .models import Neighbourhood,Business,Profile,Join,Posts,Comments
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	'''
	This view function will render the index  landing page
	'''
	if request.user.is_authenticated:
		if Join.objects.filter(user_id = request.user).exists():
			hood = Neighbourhood.objects.get(pk = request.user.join.hood_id.id)
			posts = Posts.objects.filter(hood = request.user.join.hood_id.id)
			businesses = Business.objects.filter(hood = request.user.join.hood_id.id)
			return render(request,'hood/myhood.html',{"hood":hood,"businesses":businesses,"posts":posts})
		else:
			neighbourhoods = Neighbourhood.objects.all()
			return render(request,'index.html',{"neighbourhoods":neighbourhoods})
	else:
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
			messages.success(request, 'Success! Signup was a success, now join or create a neighbourhood to start using Kaa Rada')
			return redirect('index')
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def createHood(request):
	'''
	This view function will create an instance of a neighbourhood
	'''
	if request.method == 'POST':
		form = CreateHoodForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'You Have succesfully created a hood.You may now join your neighbourhood')
			return redirect('index')

	else:
		form = CreateHoodForm()
		return render(request,'hood/create.html',{"form":form})

@login_required(login_url='/accounts/login/')
def editHood(request,hood_id):
	'''
	This view function will edit an instance of a neighbourhood
	'''
	neighbourhood = Neighbourhood.objects.get(pk = hood_id)
	if request.method == 'POST':
		form = CreateHoodForm(request.POST,instance = neighbourhood)
		if form.is_valid():
			form.save()
			messages.success(request, 'Success! You Have succesfully edited your hood')
			
			return redirect('index')
	else:
		form = CreateHoodForm(instance = neighbourhood)
		return render(request,'hood/edit.html',{"form":form,"neighbourhood":neighbourhood})

@login_required(login_url='/accounts/login/')
def createBusiness(request):
	'''
	This function will create a Business Instance
	'''
	if Join.objects.filter(user_id = request.user).exists():

		if request.method == 'POST':
			
			form = CreateBusinessForm(request.POST)
			if form.is_valid():
				business = form.save(commit = False)
				business.user = request.user
				business.hood = request.user.join.hood_id
				business.save()
				messages.success(request, 'Success! You have created a business')
				return redirect('allBusinesses')
		else:
			form = CreateBusinessForm()
			return render(request,'business/create.html',{"form":form})
				
	else:

		messages.error(request, 'Error! Join a Neighbourhood to create a Business')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def businessIndex(request):
	'''
	This post will fetch all business instances belonging to the current logged in user
	'''
	businesses= Business.objects.filter(user = request.user)
	return render(request,'business/index.html',{"businesses":businesses})

@login_required(login_url='/accounts/login/')
def profile(request):
	'''
	This view function will fetch a user's profile
	'''
	profile = Profile.objects.get(user = request.user)
	return render(request,'accounts/profile.html',{"profile":profile})
	
@login_required(login_url='/accounts/login/')
def editProfile(request):
	'''
	This view function will edit a profile instance
	'''
	profile = Profile.objects.get(user = request.user)
	if request.method == 'POST':
		form = EditprofileForm(request.POST,instance = profile )
		if form.is_valid():
			form.save()
			messages.success(request, 'Successful profile edit!')
			return redirect('profile')
	else:
		form = EditprofileForm(instance = profile )
		return render(request,'accounts/edit.html',{"form":form})
	
@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def join(request,hoodId):
	'''
	This view function will implement adding 
	'''
	neighbourhood = Neighbourhood.objects.get(pk = hoodId)
	if Join.objects.filter(user_id = request.user).exists():
		
		Join.objects.filter(user_id = request.user).update(hood_id = neighbourhood)
	else:
		
		Join(user_id=request.user,hood_id = neighbourhood).save()

	messages.success(request, 'Success! You have succesfully joined this Neighbourhood ')
	return redirect('index')

def hoodHome(request,hoodId):
	'''
	This function will retrive instances of a neighbourhood
	'''
	hood = Neighbourhood.objects.get(pk = hoodId)
	posts = Posts.objects.filter(hood = hoodId)
	businesses = Business.objects.filter(hood = hoodId)
	return render(request,'hood/myhood.html',{"hood":hood,"businesses":businesses,"posts":posts})

@login_required(login_url='/accounts/login/')
def exitHood(request,hoodId):
	'''
	This function will delete a neighbourhood instance in the join table
	'''
	if Join.objects.filter(user_id = request.user).exists():
		Join.objects.get(user_id = request.user).delete()
		messages.error(request, 'You have succesfully exited this Neighbourhood.')
		return redirect('index')

@login_required(login_url='/accounts/login/')
def createPost(request):
	'''
	This function will create a Posts instance
	'''
	if Join.objects.filter(user_id = request.user).exists():
		if request.method == 'POST':
			form = ForumPostForm(request.POST)
			if form.is_valid():
				post = form.save(commit = False)
				post.user = request.user
				post.hood = request.user.join.hood_id
				post.save()
				messages.success(request,'You have succesfully created a Forum Post')
				return redirect('index')
		else:
			form = ForumPostForm()
			return render(request,'posts/create.html',{"form":form})
	else:
		messages.error(request, 'Error! You can only create a forum post after Joining/Creating a neighbourhood')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def singlePost(request,postId):
	'''
	This view function will retrieve a single instance of a forum post
	'''
	if Join.objects.filter(user_id = request.user).exists():
		post = Posts.objects.get(id = postId)
		comments = Comments.objects.filter(post = postId)
		if request.method == 'POST':
			form = CommentForm(request.POST)
			if form.is_valid():
				comment = form.save(commit = False)
				comment.user = request.user
				comment.post = post
				comment.save()

				messages.success(request,'You have succesfully commented on this post')
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			form = CommentForm()
		return render(request,'posts/single.html',{"post":post,"form":form,"comments":comments})
	else:
		messages.error(request,'Join a neighbourhood to view this post')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def editPost(request,postId):
	'''
	This view function will edit a single post instance
	'''
	if Join.objects.filter(user_id = request.user).exists():

		post = Posts.objects.get(id = postId)
		if request.method == 'POST':
			form = ForumPostForm(request.POST,instance = post)
			if form.is_valid():
				post = form.save(commit = False)
				post.user = request.user
				post.hood = request.user.join.hood_id
				post.save()
				messages.success(request,'Succesfully edited your post')
				return redirect('singlePost',postId)
		else:
			form = ForumPostForm(instance = post)
			return render(request,'posts/edit.html',{"form":form,"post":post})
	else:
		messages.error(request,'Join a neighbourhood to edit this post')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def changeHood(request):
	'''
	View function to retrieve hood resources incase a user wants to change their current neighbourhood
	'''
	neighbourhoods = Neighbourhood.objects.all()
	return render(request,'hood/joinhood.html',{"neighbourhoods":neighbourhoods})
