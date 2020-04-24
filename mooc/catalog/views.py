from django.shortcuts import render
from catalog.models import User, Field, Course, Postedby
from django.views import generic

# Create your views here.

def index(request):
    num_courses = Course.objects.all().count()
    num_postedby = Postedby.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_courses': num_courses,
        'num_postedby': num_postedby,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class CourseListView(generic.ListView):
    model = Course
    paginate_by = 2

class CourseDetailView(generic.DetailView):
    model = Course

class PostedbyListView(generic.ListView):
    model = Postedby
    paginate_by = 2

class PostedbyDetailView(generic.DetailView):
    model = Postedby