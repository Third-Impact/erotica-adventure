from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views import generic

# from story.models import Scene, Branch
# from django.contrib.auth.models import Permission, User
# from story.forms import UserForm, LoginForm, NewSceneForm, EditSceneForm, BranchForm

# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.conf import settings
# from django.utils.decorators import method_decorator

def direct_to_index(request):
	return HttpResponseRedirect('/erotica/')

def permission_redirect(request):
	template_name = 'scene_permission.html'
	return  render(request, template_name, {})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/erotica/')
	
def about(request):
	return HttpResponse("Its about tiiiiiime")