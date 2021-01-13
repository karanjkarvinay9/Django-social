from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
	text  = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Add a Comment','autocomplete' : 'off'}))
	class Meta:
		model = Comment
		fields = ('text',)

class PostForm(forms.ModelForm):
	captions = forms.CharField(widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
	class Meta:
		model = Post
		fields = ('captions','image')
    