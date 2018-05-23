from django.db import models
import datetime as dt
from django.contrib.auth.models import User

# Create your models here.
class Business(models.Model):
	'''
	Model class that creates the Business model columnin the database
	'''
	name = models.CharField(max_length = 300)
	description = models.TextField()
	email_address = models.EmailField()

	def __str__(self):
		return self.name

class Neighbourhood(models.Model):
	'''
	Model that creates the neighbourhood column in the database
	'''
	name = models.CharField(max_length = 300)
	location = models.CharField(max_length = 100)
	population = models.IntegerField(max_length = 300)
	
	def __str__(self):
		return self.name


