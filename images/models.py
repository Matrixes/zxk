from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify


class Image(models.Model):
	user = models.ForeignKey(User, related_name='images_created')
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True)
	url = models.URLField()
	image = models.ImageField(upload_to='images/%Y/%m/%d')
	description = models.TextField(blank=True)
	created = models.DateField(auto_now_add=True, db_index=True)

	users_like = models.ManyToManyField(User, related_name='image_liked', blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
			super(Image, self).save(*args, **kwargs)