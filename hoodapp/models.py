from django.db import models
import datetime as dt
from django.contrib.auth.models import User

# Create your models here.
class Business(models.Model):
	name = models.CharField(max_length = 300)
	description = models.TextField()
	email_address = models.EmailField()
	
	def __str__(self):
		return self.name


