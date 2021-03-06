# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# 给收藏夹用的
from blog.models import Post
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# 头像上传路径及命名
def upload_path_handler(instance, filename):
	name = str(instance.id) +  '-' + filename
	return "users/{}".format(name)  # Ymd invalid


# 用户扩展资料
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	nickname = models.CharField(max_length=20, blank=True)
	# phone = models.CharField(max_length=11, blank=True)
	website = models.URLField(blank=True)
	birthday = models.DateField(blank=True, null=True)

	introduce = models.CharField(max_length=100, blank=True)

	photo = models.ImageField(upload_to=upload_path_handler, blank=True, default="users/default.png")

	def __str__(self):
		return "{}'s profile".format(self.user.username)



# 使用第三方账号登录的用户另外再保存到一张表
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


# 用户设置
class UserSetting(models.Model):
	STATUS_CHOICES = (
		('E', '富文本'),
		('M', 'Markdown'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='setting')
	setting = models.CharField(max_length=10, choices=STATUS_CHOICES, default='M')

	# 个性域名
	domain = models.CharField(max_length=20, unique=True, blank=True, null=True)

	def __str__(self):
		return "{}'s setting".format(self.user.username)


# 用户关注系统
# 将关系定义在UserProfile上也行，而且在admin上也更好管理，
# 但是会带来复杂的查询和额外的表连接
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
# using add_to_class() is not the recommended way for adding fields to models. 
# Thus, the ManyToManyField added dynamically will not
# imply any database changes for the Django User model.

# Django forces the relationship to be symmetrical.
# In this case, we are setting symmetrical=False to define a non-symmetric relation.
# This is, if I follow you, it doesn't mean you automatically follow me.

# When you use an intermediate model for many-to-many
# relationships some of the related manager's methods are disabled,
# such as add(), create() or remove(). You need to create or
# delete instances of the intermediate model instead.


# 用户的收藏夹
class Collection(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='collections')
	posts = models.ManyToManyField(Post, blank=True, related_name='collector')

	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{}'s collections.".format(self.user.username)