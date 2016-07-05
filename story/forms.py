from django import forms
from django.contrib.auth.models import User
from .models import Scene, Branch

class UserForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=75)
    password1 = forms.CharField(label='password', max_length=50)
    password2 = forms.CharField(label='password again', max_length=50)

    def clean(self):
    	cleaned_data = super(UserForm, self).clean()
    	password1 = cleaned_data.get("password1")
    	password2 = cleaned_data.get("password2")

    	if password1 != password2:
    		raise forms.ValidationError(
                    "The password fields must both be the same."
                )
    class Meta:
    	fields = ('username', 'password1', 'password2')
    	model = User


class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=75)
	password = forms.CharField( max_length=50)

	# def clean(self):
	# 	cleaned_data = super(LoginForm, self).clean()

	# class Meta:
	# 	fields = ('username', 'password')
	# 	model = User

class NewSceneForm(forms.ModelForm):
	story_text = forms.CharField(widget=forms.Textarea, label='write scene story here')

	class Meta:
		fields = ('story_text', 'save_point', 'end_point', 'picture')
		model = Scene

class EditSceneForm(forms.ModelForm):
	story_text = forms.CharField(widget=forms.Textarea, label='write scene story here')

	class Meta:
		fields = ('story_text', 'save_point', 'end_point', 'closed', 'picture')
		model = Scene