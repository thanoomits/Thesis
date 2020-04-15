from django.contrib import admin
from .models import User, Course, Teacher, Field

# Register your models here.

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Field)