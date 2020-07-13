from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import User, Field, Course, Postedby, MyCourse, Lessons
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from catalog.forms import EditProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User as AuthUser

# Create your views here.

def index(request):
    num_courses = Course.objects.all().count()
    num_users = User.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_courses': num_courses,
        'num_users': num_users,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class CourseListView(generic.ListView):
    model = Course

class CourseDetailView(generic.DetailView):
    model = Course

class UserListView(generic.ListView):
    model = User
    paginate_by = 2

class UserDetailView(generic.DetailView):
    model = User

class PostedbyCreate(CreateView):
    model = Postedby
    fields = '__all__'

class PostedbyUpdate(UpdateView):
    model = Postedby
    fields = ['posted_date', 'last_modified_date']

class PostedbyDelete(DeleteView):
    model = Postedby
    success_url = reverse_lazy('teachers')

class LessonsListView(generic.ListView):
    model = Lessons

    def get_context_data(self, **kwargs):
        context = super(LessonsListView, self).get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        context['course'] = course
        return(context)

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        
        return self.model.objects.filter(
            course=course.id
        )

class LessonsDetailView(generic.DetailView):
    model = Lessons

class ActiveCoursesByUserListView(LoginRequiredMixin, generic.ListView):
    model = MyCourse
    template_name = 'catalog/mycourse_list_active_user.html'

    def get_queryset(self):
        my_user = self.request.user
        my_user = User.objects.get(username=my_user)

        return MyCourse.objects.filter(active=my_user).filter(status__exact='i').order_by('-last_accessed')

@login_required
def addtolist(request, pk):
    course = get_object_or_404(Course, pk=pk)
    current_user = request.user
    current_user = User.objects.get(username=current_user)
    current_course = Course.objects.get(title=course.title)

    count = MyCourse.objects.filter(active=current_user, course=current_course).count()
    if count==0:
        add = MyCourse(active=current_user, course=current_course, status='i')
        add.save()
        messages.success(request, "List updated!")

        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request,"This Course is already in your list!")
        return redirect(request.META['HTTP_REFERER'])

@login_required
def deletefromlist(request, pk):
    course = get_object_or_404(Course, pk=pk)
    current_user = request.user
    current_user = User.objects.get(username=current_user)
    current_course = Course.objects.get(title=course.title)
    MyCourse.objects.get(active=current_user,course=current_course).delete()

    return redirect(request.META['HTTP_REFERER'])

@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'catalog/profile.html', args)

@login_required
def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
        
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'catalog/edit_profile.html', args)

@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('/change-password')

    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'catalog/change_password.html', args)


