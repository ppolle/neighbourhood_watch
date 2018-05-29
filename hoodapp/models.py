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
	COUNTY_CHOICES = (
('Baringo','Baringo County'),
('Bomet','Bomet County'),
('Bungoma','Bungoma County'),
('Busia','Busia County'),
('Elgeyo Marakwet','Elgeyo Marakwet County'),
('Embu','Embu County'),
('Garissa','Garissa County'),
('Homa Bay','Homa Bay County'),
('Isiolo','Isiolo County'),
('Kajiado','Kajiado County'),
('Kakamega','Kakamega County'),
('Kericho','Kericho County'),
('Kiambu','Kiambu County'),
('Kilifi','Kilifi County'),
('Kirinyaga','Kirinyaga County'),
('Kisii','Kisii County'),
('Kisumu','Kisumu County'),
('Kitui','Kitui County'),
('Kwale','Kwale County'),
('Laikipia','Laikipia County'),
('Lamu','Lamu County'),
('Machakos','Machakos County'),
('Makueni','Makueni County'),
('Mandera','Mandera County'),
('Meru','Meru County'),
('Migori','Migori County'),
('Marsabit','Marsabit County'),
('Mombasa','Mombasa County'),
('Muranga','Muranga County'),
('Nairobi','Nairobi County'),
('Nakuru','Nakuru County'),
('Nandi','Nandi County'),
('Narok','Narok County'),
('Nyamira','Nyamira County'),
('Nyandarua','Nyandarua County'),
('Nyeri','Nyeri County'),
('Samburu','Samburu County'),
('Siaya','Siaya County'),
('Taita Taveta','Taita Taveta County'),
('Tana River','Tana River County'),
('Tharaka Nithi','Tharaka Nithi County'),
('Trans Nzoia','Trans Nzoia County'),
('Turkana','Turkana County'),
('Uasin Gishu','Uasin Gishu County'),
('Vihiga','Vihiga County'),
('Wajir','Wajir County'),
('West Pokot','West Pokot County'),
   
    )
	name = models.CharField(max_length = 300)
	description = models.TextField(max_length = 300)
	location = models.CharField(max_length = 100,choices=COUNTY_CHOICES)
	population = models.IntegerField()
	user = models.ForeignKey(User)

	def save_hood(self):
		self.save()

	def delete_hood(self):
		self.delete()

	@classmethod	
	def search_hood(cls,search_term):
		hoods = cls.objects.filter(name__icontains = search_term)
		return hoods


	
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
	
	def save_biz(self):
		self.save()

	def delete_biz():
		self.delete()

	@classmethod
	def find_business(cls,search_term):
		businesses = cls.objects.filter(name__icontains = search_term)
		return businesses

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

	def save_posts(self):
		self.save()

	def delete_posts(self):
		self.delete()

	def __str__(self):
		return self.title
class Comments(models.Model):
	'''
	Model will handle comments made to a post resource
	'''
	comment = models.CharField(max_length = 600)
	user = models.ForeignKey(User)
	post = models.ForeignKey(Posts)

	def save_comment(self):
		self.save()

	def delete_comment(self):
		self.delete()

	def __str__(self):
		return self.comment


