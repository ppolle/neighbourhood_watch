from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Neighbourhood(models.Model):
	'''
	Model that creates the neighbourhood column in the database
	'''
	name = models.CharField(max_length = 300)
	description = models.TextField(max_length = 300)
	location = models.CharField(max_length = 100)
	population = models.IntegerField()
	user = models.ForeignKey(User)
	
	def __str__(self):
		return self.name

class Business(models.Model):
	'''
	Model class that creates the Business model columnin the database
	'''
	name = models.CharField(max_length = 300)
	description = models.TextField()
	email_address = models.EmailField()
	user = models.ForeignKey(User)
	hood = models.ForeignKey(Neighbourhood)
	
	def __str__(self):
		return self.name

class Profile(models.Model):
	'''
	Model that creates the profile column in the database
	'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500,default = "Awesome bio will appear here") 
	
	def __str__(self):
		return self.user

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Join(models.Model):
	'''
	Model that keeps track of what user has joined what neighbourhood
	'''
	user_id = models.OneToOneField(User)
	hood_id = models.ForeignKey(Neighbourhood)

	def __str__(self):
		return self.user_id

class Posts(models.Model):
	'''
	Model that handles posts made to a neighbourhood
	'''
	title = models.CharField(max_length = 300)
	body = models.TextField()
	user = models.ForeignKey(User)
	hood = models.ForeignKey(Neighbourhood)

	def __str__(self):
		return self.title
class Comments(models.Model):
	'''
	Model will handle comments made to a post resource
	'''
	comment = models.CharField(max_length = 600)
	user = models.ForeignKey(User)
	post = models.ForeignKey(Posts)

	def __str__(self):
		return self.comment


