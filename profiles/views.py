from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Profile, Relationship
from posts.models import Comment, Like, Post
from .forms import ProfileModelForm
from posts.forms import CommentForm
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import UpdateView 

# Create your views here.

class ProfileView(LoginRequiredMixin,View):
	def get(self,request,slug):
		user = Profile.objects.get(user = request.user)
		profile = Profile.objects.get(slug=slug)
		c_form = CommentForm()
		form = None
		if user == profile:
			form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
			status = False
		else:
			try:	
				s = get_object_or_404(Relationship,sender=user,receiver=profile)
				status = s.status

			except :
				try:
					s = get_object_or_404(Relationship,sender=profile,receiver=user)
					status = s.status
					if status=='pending':
						status = 'wating'
				except:
					status='add_friend'

		friends = profile.get_all_friends()
		friends_count = friends.count()

		try:
			posts = Post.objects.filter(author = profile)
			post_count = posts.count()
		except:
			posts = False
			post_count = 0
		# Hide or show comments in web page only
		ctx = {
		'c_form' : c_form,
		'profile': user,
		'u_form' : form,
		'f_profile' : profile,
		'status': status,
		'posts': posts,
		'post_count':post_count,
		}
		return render(request ,'profile/Profile.html', ctx)


	def post(self,request,slug):
		profile = Profile.objects.get(slug=slug)
		if  not request.user==profile.user:
			raise PermissionDenied
		form = ProfileModelForm(request.POST,request.FILES,instance=profile)
		if form.is_valid():
			form.save()
		return redirect(request.get_full_path())


# @login_required
def signup_view(request):
	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		form.save()
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('posts:post_list')
	return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile_list_view(request):
	profile = Profile.objects.get(user=request.user)
	friends = []
	temp = profile.get_all_friends()
	for t in temp:
		friends.append(Profile.objects.get(user=t))

	pending = Relationship.objects.filter(receiver=profile, status='pending')
	friends_pending =list(map(lambda x: x.sender, pending))

	wating = Relationship.objects.filter(sender=profile, status='pending')
	wating_approval =list(map(lambda x: x.receiver, wating))

	all_profile = Profile.objects.all().exclude(user__in=temp).exclude(user=request.user)

	ctx = {
	'profile':profile,
	'all_profile': all_profile,
	'friends':friends,
	'friends_pending':friends_pending,
	'wating_approval':wating_approval
	}
	return render(request, 'profile/friends.html',ctx)

	
		
@login_required
def remove_Friend(request):
	next_url = request.POST.get('next')
	profile = Profile.objects.get(user=request.user)
	friend = Profile.objects.get(id=request.POST.get('friend_id'))
	rel = Relationship.objects.get(
	(Q(sender=profile) & Q(receiver=friend)) | (Q(sender=friend) & Q(receiver=profile)))
	rel.delete()
	if next_url == 'list':
		return redirect('profiles:profile_list_view')
	else:
		return redirect(reverse('profiles:profile_view', kwargs={'slug': next_url }))



@login_required
def confirm_Friend(request):
	next_url = request.POST.get('next')
	profile = Profile.objects.get(user=request.user)
	friend = Profile.objects.get(id=request.POST.get('friend_id'))
	obj = Relationship.objects.get(sender=friend,receiver=profile)
	obj.status = 'accepted'
	obj.save()
	if next_url == 'list':
		return redirect('profiles:profile_list_view')
	else:
		return redirect(reverse('profiles:profile_view', kwargs={'slug': next_url }))


@login_required
def add_Friend(request):
	next_url = request.POST.get('next')
	profile = Profile.objects.get(user=request.user)
	friend = Profile.objects.get(id=request.POST.get('profile_id'))
	obj = Relationship.objects.create(sender=profile,receiver=friend)
	obj.status = 'pending'
	obj.save()
	if next_url == 'list':
		return redirect('profiles:profile_list_view')
	else:
		return redirect(reverse('profiles:profile_view', kwargs={'slug': next_url }))


@login_required
def new_Friend(request):
	profile = Profile.objects.get(user=request.user)
	temp = profile.get_all_friends()
	all_profile = Profile.objects.all().exclude(user__in=temp).exclude(user=request.user)

	ctx = {
	'profile':profile,
	'all_profile': all_profile,
	'friends':False,
	'friends_pending':False,
	'wating_approval':False
	}
	return render(request, 'profile/friends.html',ctx)
