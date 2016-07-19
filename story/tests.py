from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Scene, Branch
from django.test import Client
from django.utils import timezone
# Create your tests here.


class ModelTest(TestCase):
  
  @classmethod
  def setUpTestData(cls):
    cls.u1 = cls.create_user('TheDoc', 'enterthedalek', 'blah@example.come')
    cls.scene_origin = cls.create_scene("origin", False, '', cls.u1)
    print("origin id is " + str(cls.scene_origin.id))
    cls.scene_t2 = cls.create_scene("Something happens", False, '', cls.u1)
    cls.scene_t3 = cls.create_scene("Candidate endpoint", False, '', cls.u1) 

  @staticmethod
  def create_scene(story, save, pic, user):
    time = timezone.now()
    scene = Scene(story_text=story, save_point=save, picture=pic, last_edited=time, user=user)
    scene.save()
    return scene
  
  @staticmethod
  def create_user(name, password, email):
    user = User(username=name, email=email)
    user.set_password(password)
    user.save()
    return user
  
  @staticmethod
  def create_branch(from_scene, to_scene, text):
    branch = Branch(from_scene=from_scene, to_scene=to_scene, description=text)
    branch.save()
    return branch

class EndPointEligabilityTest(ModelTest):

  def test_single_new_scene_cannot_be_end(self):
    self.assertEqual(self.scene_t2.can_be_end(), False)

  def test_adding_a_branch_to_scene_can_make_endpoint(self):
    ModelTest.create_branch(self.scene_origin, self.scene_t2, "a branch")
    self.assertEqual(self.scene_t2.can_be_end(), True)

  def test_adding_a_branch_from_scene_to_origin_can_be_end(self):
    ModelTest.create_branch(self.scene_origin, self.scene_t2, "a branch")
    ModelTest.create_branch(self.scene_t2, self.scene_t3, "branch to end")
    self.assertEqual(self.scene_t2.can_be_end(), False)
    self.assertEqual(self.scene_t3.can_be_end(), True)
    ModelTest.create_branch(self.scene_t3, self.scene_origin, "branch to origin")
    self.assertEqual(self.scene_t3.can_be_end(), True)

  def test_adding_a_branch_from_scene_to_save_point_can_be_end(self):
    ModelTest.create_branch(self.scene_origin, self.scene_t2, "a branch")
    ModelTest.create_branch(self.scene_t2, self.scene_t3, "branch to end")
    self.assertEqual(self.scene_t3.can_be_end(), True)
    self.scene_t4 = ModelTest.create_scene("will be save point", False, '', self.u1)
    ModelTest.create_branch(self.scene_t3, self.scene_t4, "branch to save point")
    self.assertEqual(self.scene_t3.can_be_end(), False)
    self.scene_t4.save_point = True
    self.scene_t4.save()
    self.assertEqual(self.scene_t3.can_be_end(), True)

  def test_adding_a_branch_from_scene_to_other_will_not_be_end(self):
    ModelTest.create_branch(self.scene_origin, self.scene_t2, "a branch to end")
    self.assertEqual(self.scene_t2.can_be_end(), True)
    ModelTest.create_branch(self.scene_t2, self.scene_t3, "branch from end")
    self.assertEqual(self.scene_t2.can_be_end(), False)


  # def test_index_status(self):
  #   response = self.client.get('/erotica/')
  #   self.assertEqual(response.status_code, 200)

  # def test_single_new_scene_cannot_be_open(self):
  #   self.assertEqual(self.scene_t2.can_be_open(), False)