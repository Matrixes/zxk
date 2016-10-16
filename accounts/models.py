from django.db import models
from django.contrib.auth.models import User


def upload_path_handler(instance, filename):
	name = str(instance.id) +  '-' + filename
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


class Contack(models.Model):
	user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_from_set')
	user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_to_set')
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return "{} follows {}".format(self.user_from, self.user_to)


# If the User model was part of our application, we could add the previous field to
# the model. However, we cannot alter the User class directly because it belongs to
# the django.contrib.auth application. 

# # Add following field to User dynamically
User.add_to_class('following', models.ManyToManyField('self', 
	                                                  through=Contack,
	                                                  related_name='followers',
	                                                  symmetrical=False))
#  using add_to_class() is not the recommended way for adding fields to models. 
# 不会改变数据库？