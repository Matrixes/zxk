from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
	user = models.ForeignKey(User, related_name='actions', db_index=True)
	verb = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	# A ForeignKey field to the ContentType model.
	target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj')
	
	# A PositiveIntegerField for storing the primary key of the related object.
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