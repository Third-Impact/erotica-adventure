from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views import generic

from .models import Scene, Branch
from django.contrib.auth.models import Permission, User
from .forms import UserForm, LoginForm, NewSceneForm, EditSceneForm, BranchForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.utils import timezone

class IndexView(generic.ListView):
# def index(request):
	template_name = 'index.html'
	context_obect_name = 'scenes'
	model = Branch

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		# try:
		scenes = []
		branches = Branch.objects.filter(from_scene_id=1).values()
		for branch in branches:
			scene = Scene.objects.get(pk=branch['to_scene_id'])
			scenes.append(scene)
		# except Scene.DoesNotExist:
		# 	raise Http404("problem finding scenes")

		context['scenes'] = scenes
		# return render(request, 'index.html', {'scenes': scenes})
		return context


class SceneView(generic.DetailView):
# def show(request, scene_id):
	template_name = 'scene_show_story.html'
	context_obect_name = 'scene_and_branches'
	model = Scene


	def get_object(self):
		scene = super(SceneView, self).get_object()
		return scene

	def get_context_data(self, **kwargs):
		context = super(SceneView, self).get_context_data(**kwargs)
		context['branches'] = Branch.objects.filter(from_scene = self.kwargs['pk'])

		return context


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
			new_user = User(username= form.cleaned_data['username'])#form.save(commit=False)
			new_user.set_password(form.cleaned_data['password1'])
			new_user.save()
			return HttpResponseRedirect(self.success_url)

		return render(request, self.template_name, {'form': form})


class LoginView(generic.FormView):
	form_class = LoginForm
	default_values = {'username': '', 'password': ''}
	template_name = 'login_form.html'
	success_url = '/erotica'

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

# from django.contrib.auth.mixins import LoginRequiredMixin
@method_decorator(login_required, name='dispatch')
class SceneCreateView(generic.edit.CreateView):
	login_url = '/erotica/permission/'
	form_class = NewSceneForm
	template_name = 'new_scene_form.html'
	model = Scene

	default_values = {'story_text': '', 'save_point':False, 'end_point':False, 'picture':''}

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.default_values)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			scene = Scene(
				story_text=form.cleaned_data['story_text'],
			 	save_point=form.cleaned_data['save_point'], 
			 	end_point=form.cleaned_data['end_point'],
			 	picture=form.cleaned_data['picture'],
			 	user = request.user,
			 	last_edited=timezone.now()
			 	)
			scene.save()
			success_url = '/erotica/'+str(scene.id)+'/'
			return HttpResponseRedirect(success_url)

		return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class SceneEditView(generic.edit.UpdateView):
	model = Scene
	login_url = '/erotica/permission/'

	form_class = EditSceneForm
	template_name = 'edit_scene_form.html'

	def check_author(self, current_scene, user):
		author = current_scene.user
		if author == user:
			return True
		else:
			return False

	def get_context_data(self, **kwargs):
		context = Scene.objects.get(pk=self.kwargs['pk'])
		return context
	#@user_passes_test(check_author, redirect_field_name='/erotica/permission/')
	def get(self, request, *args, **kwargs):
		current_scene = self.get_object() #context = Scene.objects.get(pk=self.kargs['pk'])
		scene_values = {
			'story_text':current_scene.story_text,
			'save_point':current_scene.save_point,
			'end_point':current_scene.end_point,
			'picture':current_scene.picture
		}
		#author = current_scene.user
		if self.check_author(current_scene, request.user):
			form = self.form_class(initial=scene_values)
			return render(request, self.template_name, {'form': form, 'scene': current_scene})
		else:
			return render(request, 'scene_permission.html', {'scene': current_scene})
	# @user_passes_test(check_author)
	def post(self, request, *args, **kwargs):
		edited_scene = self.get_object()
		if self.check_author(edited_scene, request.user):
			
			form = self.form_class(request.POST)
			if form.is_valid() and self.params_ok(form):
				edited_scene.story_text = form.cleaned_data['story_text']
				edited_scene.save()

				success_url = '/erotica/'+str(edited_scene.id)+'/'
				return HttpResponseRedirect(success_url)

			return render(request, self.template_name, {'form': form, 'scene': edited_scene})
		else:
			return render(request, 'scene_permission.html', {'scene': current_scene, 'author':False})

	#checks the edited scene paramters to make sure they are kosher
	def params_ok(self, form):
		#check end point
		#check if scene could be opened
		return True

@method_decorator(login_required, name='dispatch')
class BranchCreateView(generic.edit.CreateView):
	model = Branch
	login_url = '/erotica/permission/'
	form_class = BranchForm
	template_name = 'branch_form.html'
	
	def get_form_contents(self, request, form):
		querytext = "user_id=" + str(request.user.id) + " or closed=False"
		valid_scenes = Scene.objects.extra(where=[querytext])
		from_scene = Scene.objects.get(pk=self.kwargs['pk'])
		# content = form.generate_choices(request.user, pk=self.kwargs['pk'])
		# content['form'] = form
		return {'form': form, 'defval':from_scene, 'scenes':valid_scenes}

	def get(self, request, *args, **kwargs):
		from_scene = Scene.objects.get(pk=self.kwargs['pk'])
		default_values = {'from_scene': from_scene}
		form = self.form_class(initial=default_values)
		# self.generate_choices(request.user)
		content = self.get_form_contents(request, form)
		if from_scene.closed == False or from_scene.user == request.user:
			return render(request, self.template_name, content)
		else:
			return render(request, 'scene_permission.html', {'scene': from_scene})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			selected_scene_to = form.cleaned_data['to_scene']
			selected_scene_from = form.cleaned_data['from_scene']
			selected_description = form.cleaned_data['description']

			current_user = request.user#This should no longer be needed, because only authored and open scenes available as choices
			if selected_scene_to.closed == False or selected_scene_to.user == current_user:
				
				branch = Branch(
					to_scene=selected_scene_to,
					from_scene=selected_scene_from,
					description=selected_description
					)
				branch.save()
				success_url = '/erotica/'+str(self.kwargs['pk'])+'/'
				return HttpResponseRedirect(success_url)
			
			else:
				form.add_error(field=None, error="A branch can only be created to an open scene or one you have written")
				content = self.get_form_contents(request, form)
				return render(request, self.template_name, content)

		content = self.get_form_contents(request, form)
		return render(request, self.template_name, content)		

def permission_redirect(request):
	template_name = 'scene_permission.html'
	return  render(request, template_name, {})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/erotica/')
	
def about(request):
	return HttpResponse("Its about tiiiiiime")