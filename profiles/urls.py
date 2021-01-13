from django.urls import path
from .views import *

app_name= 'profiles'

urlpatterns = [
	path('register/',signup_view, name='register'),
	path('Friends/',profile_list_view, name='profile_list_view'),
	path('connect/',new_Friend, name='new_friend'),
	path('remove/friend/',remove_Friend, name='remove_friend'),
	path('confirm/friend/',confirm_Friend, name='confirm_friend'),
	path('add/friend/',add_Friend, name='add_friend'),
	path('<slug>/',ProfileView.as_view(), name='profile_view'),
]