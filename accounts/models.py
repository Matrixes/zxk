from django.db import models
from django.contrib.auth.models import User


def upload_path_handler(instance, filename):
	name = str(instance.user.id) +  '-' + filename
	return "users/{}".format(name)  # Ymd invalid


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	nickname = models.CharField(max_length=20, blank=True)
	phone = models.CharField(max_length=11, blank=True)
	website = models.URLField(blank=True)
	birthday = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to=upload_path_handler, default="users/default.png")


	def __str__(self):
		return "{}'s UserProfile".format(self.user.username)


class SocialUser(models.Model):
	choices = (
		('GH', 'github'),
		('WX', 'weixin'),
		('QQ', 'qq'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_user')
	
	login = models.CharField(max_length=50)
	social_id = models.IntegerField()

	belong = models.CharField(max_length=10, choices=choices)

	def __str__(self):
		return "{}-{}".format(self.belong, self.login)

	class Meta:
		ordering = ['belong', 'login']