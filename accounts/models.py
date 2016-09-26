from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	nickname = models.CharField(max_length=20, blank=True)
	phone = models.IntegerField(blank=True)
	birthday = models.DateField(blank=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

	def __str__(self):
		return "{}'s UserProfile".format(self.user.username)