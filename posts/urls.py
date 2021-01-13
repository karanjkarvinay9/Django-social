from django.urls import path, include 
from .views import *

app_name= 'posts'

urlpatterns = [
	path('',PostListView.as_view(), name='post_list'),
	path('addpost/',addPost, name='addpost'),
	path('like-unlike-post/',like_post, name='likepost'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='deletepost'),
]