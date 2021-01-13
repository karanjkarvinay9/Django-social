from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile, Relationship

# Create your models here.
class Post(models.Model):
	captions = models.TextField(blank=True)
	image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
	liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

	def __str__(self):
		return f"{self.author.first_name}"+str(self.captions)

	def get_all_comment(self):
		return self.comment.all()

	def get_all_comment_count(self):
		return self.comment.all().count()

	def get_all_likes(self):
		return self.liked.all()

	def get_all_likes_count(self):
		return self.liked.all().count()

	class Meta:
		ordering = ('-created_at',)



class Comment(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comment')
	text = models.TextField(max_length=300)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

	def __str__(self):
		return f"{self.text}"

	class Meta:
		ordering = ('-created_at',)



class Like(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='like')
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

	class Meta:
		unique_together = ('user','post')
