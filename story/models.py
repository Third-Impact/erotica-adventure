from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator

def picture_validator(value):
		if value is not '':
			value.URLValidator.__call__(value)
# Create your models here.
class Scene(models.Model):
	story_text = models.TextField()
	closed = models.BooleanField(default=True)
	end_point = models.BooleanField(default=False)
	save_point = models.BooleanField(default=False)
	picture = models.URLField(blank=True, validators=[picture_validator])
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	last_edited = models.DateTimeField('last changed')


	def can_be_open(self):
		branches_from = Branch.objects.filter(from_scene=self.id)
		branches_to = Branch.objects.filter(to_scene=self.id)
		if (self.end_point==True):
			if len(branches_to) >= 1:
				return True
		elif len(branches_to) >= 1 and len(branches_from) >= 2:
			return True
		else:
			return False

	def can_be_start(self):
		branches_to = Branch.objects.filter(to_scene=self.id)
		if len(branches_to) > 1:
			return False
		else:
			for branch in branches_to:
				scene_to = branch.from_scene
				if scene_to.id != 1:
					return False
		return True

	def can_be_end(self):
		branches_to = Branch.objects.filter(to_scene=self.id)
		branches_from = Branch.objects.filter(from_scene=self.id)
		if len(branches_to) < 1:
			return False
		else:
			for branch in branches_from:
				scene_to = branch.from_scene
				if scene_to.id != 1 or scene_to.save_point == False:
					return False
		return True


	def __str__(self):
		return self.story_text

class Branch(models.Model):
	from_scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="from_scene")
	to_scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="to_scene")
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.description