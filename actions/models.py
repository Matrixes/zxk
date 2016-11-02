from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
	user = models.ForeignKey(User, related_name='actions', db_index=True)
	verb = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	# A ForeignKey field to the ContentType model.
	# The usual name for this field is “content_type”.
	target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj')

	# A PositiveIntegerField for storing the primary key of the related object.
	# a field that can store primary key values from the models you’ll be relating to. 
	# The usual name for this field is “object_id”.
	target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

	# A GenericForeignKey field to the related object based on the
	# combination of the two previous fields.
	target = GenericForeignKey('target_ct', 'target_id')

	"""
	Django does not create any field in the database for GenericForeignKey fields. The
	only fields that are mapped to database fields are target_ct and target_id. Both
	fields have blank=True and null=True attributes so that a target object is not
	required when saving Action objects.
	"""

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return "{}{}{}".format(self.user.username, self.verb, self.target)

# 收藏夹，这个方法没有成功实现
"""
class Collections(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')

	content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='collections')
	object_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

	collect = GenericForeignKey('content_type', 'object_id')

	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return "{}{}".format(self.user.username, self.collect)
"""