from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views import generic

from story.models import Scene, Branch
from django.contrib.auth.models import Permission, User
from story.forms import UserForm, LoginForm, NewSceneForm, EditSceneForm, BranchForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.utils import timezone


class UserFormView(generic.View):
	form_class = UserForm
	default_values = {'username': '', 'password': ''}
	template_name = 'new_user_form.html'
	success_url = '/erotica/login'

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.default_values)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			new_user = User(username= form.cleaned_data['username'], email=form.cleaned_data['email'])#form.save(commit=False)
			new_user.set_password(form.cleaned_data['password1'])
			new_user.save()
			return HttpResponseRedirect(self.success_url)

		return render(request, self.template_name, {'form': form})


class LoginView(generic.FormView):
	form_class = LoginForm
	default_values = {'username': '', 'password': ''}
	template_name = 'login_form.html'
	success_url = '/erotica/'

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.default_values)
		return render(request, self.template_name, {'form': form})
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			name = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=name, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					# check if user has any scenes....(not done yet)
					return HttpResponseRedirect(self.success_url)
				else:
					#return HttpResponse('Bad User')
					return render(request, self.template_name, {'form': form})

			else:
				#errors = "The username or pasword is incorrect"
				form.add_error(field=None, error="The username or pasword is incorrect")
				return render(request, self.template_name, {'form': form})		

		return render(request, self.template_name, {'form': form})



@method_decorator(login_required, name='dispatch')
class AuthorScenesView(generic.ListView):

	template_name = 'author_dashboard.html'
	context_obect_name = 'author'
	model = Scene

	# def get(self, request, *args, **kwargs):
	# 	author = request.user
	# 	scenes = Scene.objects.filter(user=author).exclude(pk=1)
	# 	context = {'author': author, 'scenes':scenes}
	# 	return render(request, self.template_name, context)
	def get_context_data(self, **kwargs):
		context = super(AuthorScenesView, self).get_context_data(**kwargs)
		author = self.request.user
		context['author'] = author
		context['scenes'] = Scene.objects.filter(user=author).exclude(pk=1)
		return context
