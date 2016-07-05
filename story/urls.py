from django.conf.urls import url

from . import views

app_name = 'erotica'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new_user/$', views.UserFormView.as_view(), name='new-user'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    
    url(r'^new_scene/$', views.SceneCreateView.as_view(), name='new_scene'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.SceneEditView.as_view(), name='edit_scene'),

    url(r'^(?P<pk>[0-9]+)/branch/$', views.BranchCreateView.as_view(), name='branch'),

    url(r'^permission/$', views.permission_redirect, name='permission'),
    url(r'^about/', views.about, name='about'),
    
    url(r'^1/$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.SceneView.as_view(), name='show')

]