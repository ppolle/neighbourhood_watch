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
	description = models.TextField(max_length = 300,default = "nairobi")
	location = models.CharField(max_length = 100)
	population = models.IntegerField()
	
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
	user_id = models.ForeignKey(User)
	hood_id = models.ForeignKey(Neighbourhood)

	def __str__(self):
		return self.user_id



