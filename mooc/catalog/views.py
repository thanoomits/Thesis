from django.shortcuts import render
from catalog.models import User, Field, Course, Postedby, MyCourse
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin   

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

class UserListView(generic.ListView):
    model = User
    paginate_by = 2

class UserDetailView(generic.DetailView):
    model = User

#class PostedbyListView(generic.ListView):
#    model = Postedby
#    paginate_by = 2

#class PostedbyDetailView(generic.DetailView):
#    model = Postedby

class PostedbyCreate(CreateView):
    model = Postedby
    fields = '__all__'

class PostedbyUpdate(UpdateView):
    model = Postedby
    fields = ['posted_date', 'last_modified_date']

class PostedbyDelete(DeleteView):
    model = Postedby
    success_url = reverse_lazy('teachers')

class ActiveCoursesByUserListView(LoginRequiredMixin, generic.ListView):
    model = MyCourse
    template_name = 'catalog/mycourse_list_active_user.html'
    paginate_by = 2

    def get_queryset(self):
        return MyCourse.objects.filter()
        return MyCourse.objects.filter(active=self.user).filter(status__exact='i').order_by(last_accessed)


