from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from profiles.models import Profile, Relationship
from .models import Post, Comment, Like
from .forms import CommentForm, PostForm
from django.views.generic.edit import DeleteView 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class PostListView(LoginRequiredMixin,View):
	def  get(self, request):
		user = request.user
		profile = Profile.objects.get(user = user)
		friends = profile.get_all_friends()
		posts = []
		for friend in friends:
			temp = Profile.objects.get(user=friend)
			posts += Post.objects.filter(author = temp)

		c_form = CommentForm()
		p_form = PostForm()
		ctx={
		'profile':profile,
		'posts' : posts,
		'c_form': c_form,
		'p_form':p_form
		}
		return render(request,"post/Homepage.html", ctx)


	def post(self, request):

		user = request.user
		profile = Profile.objects.get(user = user)
		friends = profile.get_all_friends()
		posts = []
		for friend in friends:
			temp = Profile.objects.get(user=friend)
			posts += Post.objects.filter(author = temp)

		c_form = CommentForm(request.POST or None)
		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.user =profile
			post_id = request.POST.get('post_id')
			instance.post = Post.objects.get(id=post_id)
			instance.save()
			if request.is_ajax():
				return JsonResponse({
					'text': instance.text,
					'name': profile.__str__(),
					'url' : 'profile/'+profile.slug
					})

		return redirect('posts:post_list')



class PostDeleteView(LoginRequiredMixin,DeleteView):
	model = Post
	template_name = 'post/confirm_delete.html'
	success_url = reverse_lazy('posts:post_list')
	# success_url = '/posts/'

	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Post.objects.get(pk=pk)
		if not obj.author.user == self.request.user:
			messages.warning(self.request, 'You need to be the author of the post in order to delete it')
		return obj



@login_required
def addPost(request):
	profile = Profile.objects.get(user=request.user)
	f = PostForm(request.POST,request.FILES)
	if f.is_valid():

		instance = f.save(commit=False)
		instance.author = profile
		instance.save()
	return redirect('posts:post_list')



@login_required
def like_post(request):
	p_id = request.POST.get('post_id')
	post = Post.objects.get(id=p_id)
	profile = Profile.objects.get(user=request.user)
	if profile in post.liked.all():
		instance = Like.objects.get(user=profile,post=post).delete()
	else:
		instance = Like.objects.create(user=profile,post=post)
		instance.save()
	return JsonResponse({'status' : 'ok'})