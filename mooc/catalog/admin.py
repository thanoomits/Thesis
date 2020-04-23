from django.contrib import admin
from .models import User, Course, Postedby, Field

# Register your models here.

admin.site.register(User)
#admin.site.register(Course)
#admin.site.register(Postedby)
#admin.site.register(Field)

class PostedbyAdmin(admin.ModelAdmin):
    list_display = ('op', 'posted_date', 'last_modified_date')
admin.site.register(Postedby, PostedbyAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'summary', 'display_field')
admin.site.register(Course, CourseAdmin)

class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')
admin.site.register(Field, FieldAdmin)

#class UserAdmin(admin.ModelAdmin):
    #list_display = ('last_name', 'first_name', 'born_date', 'username', ' email')
    #fields = [('first_name', 'last_name'), 'username', 'email', 'born_date']
#admin.site.register(User, UserAdmin)