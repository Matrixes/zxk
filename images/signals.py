from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


"""
pre_save and post_save: Sent before or after calling the save() method of a model
re_delete and post_delete: Sent before or after calling the delete() method of a model or QuerySet
m2m_changed: Sent when a ManyToManyField on a model is changed
"""

# Django comes with a signal dispatcher that allows receiver functions to 
# get notified when certain actions occur. 
@receiver(m2m_changed, sender=Image.users_like.through)
def user_like_changed(sender, instance, **kwargs):
	instance.total_likes = instance.users_like.count()
	instance.save()

# First, we register the users_like_changed function as a receiver function using
# the receiver() decorator and we attach it to the m2m_changed signal.

# We connect the function to Image.users_like.through so that the function is only 
# called if the m2m_changed signal has been launched by this sender. 

# There is an alternate method for registering a receiver function, which consists 
# of using the connect() method of the Signal object.