from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
	def get_quertset(self):
		return super(PublishedManager, self).get_queryset().filter(status='p')


class Post(models.Model):
	STATUS_CHOICES = (
		('D', 'Draft'),
		('P', 'Published'),
	)

	title = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128, unique_for_date='publish')
	author = models.ForeignKey(User, related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='D')

	# objects = models.Manager()  # default
	published = PublishedManager()

	class Meta:
		ordering = ['-publish']

	def __str__(self):
		return self.title