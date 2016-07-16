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
		context['branches'] = branches
		# return render(request, 'index.html', {'scenes': scenes})
		return context

		# if bad_mojo:
		# 	logger.debug()


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

@method_decorator(login_required, name='dispatch')
class SceneCreateView(generic.edit.CreateView):
	login_url = '/erotica/permission/'
	form_class = NewSceneForm
	template_name = 'new_scene_form.html'
	model = Scene

	default_values = {'save_point':False, 'end_point':False, 'picture':''}

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.default_values)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			scene = Scene(
				story_text=form.cleaned_data['story_text'],
			 	save_point=form.cleaned_data['save_point'], 
			 	#end_point=form.cleaned_data['end_point'],
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
			'picture':current_scene.picture,
			'closed':current_scene.closed
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
			if form.is_valid() and self.params_ok(form, edited_scene):
				edited_scene.story_text = form.cleaned_data['story_text']
				edited_scene.save_point = form.cleaned_data['save_point']
				edited_scene.end_point = form.cleaned_data['end_point']
				edited_scene.closed = form.cleaned_data['closed']
				edited_scene.picture = form.cleaned_data['picture']
				edited_scene.last_edited = timezone.now()
				
				edited_scene.save()

				success_url = '/erotica/'+str(edited_scene.id)+'/'
				return HttpResponseRedirect(success_url)

			return render(request, self.template_name, {'form': form, 'scene': edited_scene})
		#Scene was written by a different author
		else:
			return render(request, 'scene_permission.html', {'scene': current_scene, 'author':False})

	#checks the edited scene paramters to make sure they are kosher
	def params_ok(self, form, scene):
		#check end point
		if form.cleaned_data['end_point']==True and not scene.can_be_end():
			form.add_error(field='end_point',error=
				"Scene does not meet criteria for end point."
				"Must have a branch to, and only branches from either origin or save point"
				)
			return False
		#check if scene could be opened
		if form.cleaned_data['closed']==False and not scene.can_be_open():
			form.add_error(field='closed',error=
				"Scene does not meet criteria to be open. Must have a branch linking to it; must have either 2 branches from it or designated as an end point."
				)
			return False

		return True


