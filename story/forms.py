from django import forms
from django.contrib.auth.models import User
from .models import Scene, Branch
from django.core.validators import URLValidator, EmailValidator
from django.forms import widgets

class UserForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=75)
    password1 = forms.CharField(label='password', max_length=50, widget=widgets.PasswordInput)
    password2 = forms.CharField(label='password again', max_length=50, widget=widgets.PasswordInput)
    email = forms.EmailField(label='email address')

    def clean(self):
    	cleaned_data = super(UserForm, self).clean()
    	password1 = cleaned_data.get("password1")
    	password2 = cleaned_data.get("password2")

    	if password1 != password2:
    		raise forms.ValidationError(
                    "The password fields must both be the same."
                )
    class Meta:
    	fields = ('username', 'password1', 'password2', 'email')
    	model = User


class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=75)
	password = forms.CharField( max_length=50, widget=widgets.PasswordInput)



class NewSceneForm(forms.ModelForm):
	story_text = forms.CharField(widget=forms.Textarea, label='write scene story here')

	class Meta:
		fields = ('story_text', 'save_point', 'picture')
		model = Scene


class EditSceneForm(forms.ModelForm):
	story_text = forms.CharField(widget=forms.Textarea, label='write scene story here')

	class Meta:
		fields = ('story_text', 'save_point', 'end_point', 'closed', 'picture')
		model = Scene


class BranchForm(forms.ModelForm):
	description = forms.CharField(label='Describe where the branch leads to', max_length=300)
	from_scene = forms.ModelChoiceField(queryset=Scene.objects.all())
	to_scene = forms.ModelChoiceField(queryset=Scene.objects.all())

	def clean(self):
		cleaned_data = super(BranchForm, self).clean()
		scene_from = cleaned_data.get("from_scene")
		scene_to = cleaned_data.get("to_scene")

		if scene_from == scene_to:
			raise forms.ValidationError(
    			"A branch cannot lead to itself"
				)

		if scene_from.end_point and not (scene_to.save_point or scene_to.id == 1):
			raise forms.ValidationError(
				"An end point can only branch to a save point or the origin"
				)

	class Meta:
		fields = ('from_scene', 'to_scene', 'description')
		model = Branch