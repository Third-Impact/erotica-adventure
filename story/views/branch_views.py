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
# from django.utils import timezone

@method_decorator(login_required, name='dispatch')
class BranchCreateView(generic.edit.CreateView):
	model = Branch
	login_url = '/erotica/permission/'
	form_class = BranchForm
	template_name = 'branch_form.html'
	
	def get_form_contents(self, request, form):
		querytext = "user_id=" + str(request.user.id) + " or closed=False or id=1"
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