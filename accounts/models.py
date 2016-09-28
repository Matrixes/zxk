from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	nickname = models.CharField(max_length=20, blank=True)
	phone = models.CharField(max_length=11, blank=True)
	website = models.URLField(blank=True)
	birthday = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)


	def __str__(self):
		return "{}'s UserProfile".format(self.user.username)


class SocialUser(models.Model):
	choices = (
		('GH', 'github'),
		('WX', 'weixin'),
		('QQ', 'qq'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_user')
	name = models.CharField(max_length=50)
	belong = models.CharField(max_length=10, choices=choices)

	def __str__(self):
		return "{}-{}".format(self.belong, self.name)

	class Meta:
		ordering = ['belong', 'name']