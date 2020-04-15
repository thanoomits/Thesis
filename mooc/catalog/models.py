from django.db import models
from django.urls import reverse

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
    password = models.CharField(max_length=50)   

    class Meta:
        ordering = ['last_name', 'first_name', 'username', 'email']
    
    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.username}, {self.email}'
    

class Teacher(models.Model):
    op = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.op}'
    
    def get_absolute_url(self):
        return reverse('teacher-details', args=[str(self.op)])

class Course(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the course')
    field = models.ManyToManyField(Field, help_text='Select a field for this course')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})
    