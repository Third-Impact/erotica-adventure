from django.test import TestCase
from django.contrib.auth.models import User
from .models import Scene, Branch
from django.test import Client
from django.utils import timezone
# Create your tests here.
def create_scene(story, save, pic, user):
	time = timezone.now()
	scene = Scene(story_text=story, save_point=save, picture=pic, last_edited=time, user=user)
	scene.save()
	return scene

def create_user(name, password, email):
	user = User(username=name, email=email)
	user.set_password(password)
	user.save()
	return user

def create_branch(from_scene, to_scene, text):
	branch = Branch(from_scene=from_scene, to_scene=to_scene, description=text)
	branch.save()
	return branch

class SimpleTest(TestCase):

	# fixtures = ['dump.json']
	@classmethod
	def setUpTestData(cls):
		cls.u1 = create_user('TheDoc', 'enterthedalek', 'blah@example.come')
		# cls.u1 = u1
		cls.scene_origin = create_scene("origin", False, '', cls.u1)
		cls.scene_t2 = create_scene("Something happens", False, '', cls.u1) 

	def test_index_status(self):
		response = self.client.get('/erotica/')
		self.assertEqual(response.status_code, 200)

	def single_new_scene_cannot_be_open(self):
		self.assertEqual(self.scene_t2.can_be_open(), False)