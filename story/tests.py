
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

class EndPointEligabilityTest(TestCase):

	# fixtures = ['dump.json']
	@classmethod
	def setUpTestData(cls):
		cls.u1 = create_user('TheDoc', 'enterthedalek', 'blah@example.come')
		# cls.u1 = u1
		cls.scene_origin = create_scene("origin", False, '', cls.u1)
		print("origin id is " + str(cls.scene_origin.id))
		cls.scene_t2 = create_scene("Something happens", False, '', cls.u1) 

	# def test_index_status(self):
	# 	response = self.client.get('/erotica/')
	# 	self.assertEqual(response.status_code, 200)

	# def test_single_new_scene_cannot_be_open(self):
	# 	self.assertEqual(self.scene_t2.can_be_open(), False)

	def test_single_new_scene_cannot_be_end(self):
		self.assertEqual(self.scene_t2.can_be_end(), False)

	def test_adding_a_branch_to_scene_can_make_endpoint(self):
		create_branch(self.scene_origin, self.scene_t2, "a branch")
		self.assertEqual(self.scene_t2.can_be_end(), True)

	def test_adding_a_branch_from_scene_to_origin_can_be_end(self):
		create_branch(self.scene_origin, self.scene_t2, "a branch")
		self.scene_t3 = create_scene("Candidate endpoint", False, '', self.u1)
		self.assertEqual(self.scene_t2.can_be_end(), True)
		create_branch(self.scene_t2, self.scene_t3, "branch to end")
		self.assertEqual(self.scene_t2.can_be_end(), False)
		self.assertEqual(self.scene_t3.can_be_end(), True)
		create_branch(self.scene_t3, self.scene_origin, "branch to origin")
		self.assertEqual(self.scene_t3.can_be_end(), True)