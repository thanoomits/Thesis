from django.contrib import admin
from .models import User, Course, Postedby, Field, MyCourse, Lessons, Profile, Badges, UserBadge

# Register your models here.

#admin.site.register(User)
#admin.site.register(Course)
#admin.site.register(Postedby)
#admin.site.register(Field)
#admin.site.register(MyCourse)

# admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(Badges)
admin.site.register(UserBadge)


class PostedbyAdmin(admin.ModelAdmin):
    list_display = ('op', 'posted_date', 'last_modified_date')
admin.site.register(Postedby, PostedbyAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'summary', 'display_field')
admin.site.register(Course, CourseAdmin)

class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')
admin.site.register(Field, FieldAdmin)

class MyCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'active', 'last_accessed')
    list_filter = ('status', 'last_accessed')
admin.site.register(MyCourse, MyCourseAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'born_date', 'username', 'email')
    fields = [('first_name', 'last_name'), 'username', 'email', 'born_date']
admin.site.register(User, UserAdmin)

admin.site.register(Lessons)

