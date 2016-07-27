from django.contrib import admin

# Register your models here.
from .models import Scene, Branch
admin.site.register(Scene)
admin.site.register(Branch)