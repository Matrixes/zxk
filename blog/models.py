# -*-coding:utf8 -*-


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# from django.core.urlresolvers import reverse
from django.shortcuts import reverse

# from taggit.managers import TaggableManager


class Tag(models.Model):
	name = models.CharField(max_length=10, unique=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='P')


class Post(models.Model):
	STATUS_CHOICES = (
		('D', 'Draft'),
		('P', 'Published'),
	)

	title = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128, unique_for_date='publish')
	author = models.ForeignKey(User, related_name='blog_posts')
	tags = models.ManyToManyField(Tag, related_name='blog_tags')

	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='D')

	viewed = models.IntegerField(default=0)

	objects = models.Manager()  # default，也要加上，没有的话无法用objects
	published = PublishedManager()

	#tags = TaggableManager()

	def get_absolute_url(self):
		return reverse('blog:post', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-publish']

	"""
	def save(self, *args, **kwargs):
	if not self.slug:
		self.slug = slugify(self.title)
		super(Image, self).save(*args, **kwargs)
	"""


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')
	name = models.ForeignKey(User, related_name='comments')
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return "Comment By {} on {}".format(self.name, self.post)

	class Meta:
		ordering = ['created']