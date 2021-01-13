from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete' : 'off'})) 
	last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete' :'off'}))
	bio = forms.CharField(label="About",widget=forms.TextInput(attrs={'autocomplete' :'off'}))
	avatar = forms.ImageField(label='Change Profile Picture' ,widget=forms.FileInput)
	class Meta:
		model = Profile
		fields = ('first_name', 'last_name', 'bio', 'avatar')
