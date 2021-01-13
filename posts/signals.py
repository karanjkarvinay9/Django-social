from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post, Like
import os
from django.conf import settings

@receiver(pre_delete, sender=Post)
def pre_delete_remove_files(sender, instance, **kwargs):
	name = str(instance.image)
	print(name)
	os.remove(os.path.join(settings.MEDIA_ROOT,name ))


@receiver(post_save, sender=Like)
def post_save_add_to_like(sender, instance, created, **kwargs):
	post = instance.post
	user = instance.user
	post.liked.add(user)


@receiver(pre_delete, sender=Like)
def pre_delete_remove_files(sender, instance, **kwargs):
	post = instance.post
	user = instance.user
	post.liked.remove(user)