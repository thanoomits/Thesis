from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from pinax.badges.base import Badge, BadgeAwarded
from pinax.badges.registry import badges

# Create your models here.
class Field(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a field (e.g. Physics) ')
    info = models.CharField(max_length=600, help_text='Enter some info about the field')

    def __str__(self):
        return f'{self.name}'        

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=50)

    class Meta:
        ordering = ['last_name', 'first_name', 'username', 'email']
    
    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.username}, {self.email}'
    
class Course(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the course')
    field = models.ManyToManyField(Field, help_text='Select a field for this course')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})

    def display_field(self):
        return ', '.join(field.name for field in self.field.all()[:3])
    display_field.short_description = 'Field'

class Postedby(models.Model):
    class Meta:
        verbose_name_plural = "Posted by"
    
    op = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    posted_date = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.op},{self.courses}'
    
    def get_absolute_url(self):
        return reverse('teacher-detail', kwargs={'pk': self.pk})
    
class MyCourse(models.Model):
    active = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    last_accessed = models.DateField(auto_now=True)

    CURRENT_STATUS = (
        ('n', 'Not started'),
        ('i', 'Incomplete'),
        ('c', 'Completed'),
    )

    status = models.CharField(
        max_length=1,
        choices=CURRENT_STATUS,
        blank=True,
        default='n',
        help_text='Courses taken'
    )

    class Meta:
        ordering = ['last_accessed']


    def __str__(self):
        return f'{self.course.title}'


class Lessons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField(max_length=150 , help_text='Lesson title')
    text = models.TextField(max_length=10000 , help_text='Helping text or other infomartion that you want on display', default='')
    arxeio = models.FileField(upload_to='media')
    order = models.PositiveSmallIntegerField(blank=False, null=False, default=0)


    CURRENT_STATUS = (
        ('n', 'Not started'),
        ('i', 'Incomplete'),
        ('c', 'Completed'),
    )

    status = models.CharField(
        max_length=1,
        choices=CURRENT_STATUS,
        blank=True,
        default='n',
        help_text='Courses taken'
    )

    class Meta:
        verbose_name_plural = "Lessons"
        ordering = ['order',]

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('lesson-detail', kwargs={'pk': self.pk})


class PointsBadge(Badge):
    slug = "points"
    levels = [
        "Bronze",
        "Silver",
        "Gold",
    ]
    events = [
        "points_awarded",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        points = user.profile.points
        if points > 500:
            return BadgeAwarded(level=3)
        elif points > 50:
            return BadgeAwarded(level=2)
        elif points > 5:
            return BadgeAwarded(level=1)

badges.register(PointsBadge)

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    points = models.IntegerField (
        default = 0
    )

    def award_points (self, points):
        self.points += points
        self.save()