from django.db import models
from django.contrib.auth.models import User
from social.utils import get_random_code
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.db.models import Q


class Profile(models.Model):
	first_name  = models.CharField (max_length=200)
	last_name = models.CharField (max_length=200,blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=300,blank=True)
	email = models.EmailField(max_length=200)
	country = models.CharField(max_length=50)
	# avatar = models.BinaryField(null=True, blank=True, editable=True)
	avatar = models.ImageField(default='avatar.jfif',upload_to='avatars/')
	slug = models.SlugField(unique=True, blank=True)
	friends = models.ManyToManyField(User, blank=True, related_name='friends')
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}({self.user.username})"

	
	def get_absolute_url(self):
		return reverse("profiles:profile_view", kwargs={"slug": self.slug})

	
	def get_all_friends(self):
		return self.friends.all()


	def get_friends_count(self):
		return self.friends.all().count()


	def save(self, *args, **kwargs):
		to_slug = str(self.user)
		self.slug = to_slug
		super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('pending', 'pending'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
	sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
	status = models.CharField(max_length=8, choices=STATUS_CHOICES)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f"{self.sender}-{self.receiver}"


	@classmethod
	def get_obj(self,profile,friend):
		return self.objects.get(
	(Q(sender=profile) & Q(receiver=friend)) | (Q(sender=friend) & Q(receiver=profile)))