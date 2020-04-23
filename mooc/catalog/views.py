from django.shortcuts import render
from catalog.models import User, Field, Course, Postedby
from django.views import generic

# Create your views here.

def index(request):
    num_courses = Course.objects.all().count()
    num_postedby = Postedby.objects.all().count()

    context = {
        'num_courses': num_courses,
        'num_postedby': num_postedby,
    }

    return render(request, 'index.html', context=context)

class CourseListView(generic.ListView):
    model = Course
    paginate_by = 2

class CourseDetailView(generic.DetailView):
    model = Course
