from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import User, Field, Course, Postedby, MyCourse, Lessons, PointsBadge, Profile, Badges, UserBadge
from django.views import generic
from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from catalog.forms import EditProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User as AuthUser
from django.core.paginator import Paginator
from pinax.points.models import award_points
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import ProfileSerializer, UserSerializer, MyCourseSerializer, LessonsSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


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

def about(request):
    return render(request,'about_page.html')

class CourseListView(generic.ListView):
    model = Course

class CourseDetailView(generic.DetailView):
    model = Course

class UserListView(generic.ListView):
    model = User

class PostedbyListView(generic.ListView):
    model = Postedby

class PostedbyDetailView(generic.DetailView):
    model = Postedby

    def get_context_data(self, **kwargs):
        context = super(PostedbyDetailView, self).get_context_data(**kwargs)
        teacher = self.get_object()
        teacher = User.objects.get(username=teacher.op.username)
        context['teacher'] = teacher
        context['courses'] = Course.objects.filter(teacher=teacher)
        return(context)


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

from pinax.badges.registry import badges

class LessonsDetailView(generic.DetailView):
    model = Lessons

    def get_context_data(self, **kwargs):
        context = super(LessonsDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        current_user = User.objects.get(username=user)
        profile = Profile.objects.get(user=current_user.pk)

        context['profile'] = profile
        context['xrhsths'] = user.id
        return(context)


class ActiveCoursesByUserListView(LoginRequiredMixin, generic.ListView):
    model = MyCourse
    template_name = 'catalog/mycourse_list_active_user.html'

    def get_queryset(self):
        my_user = self.request.user
        my_user = User.objects.get(username=my_user)

        return MyCourse.objects.filter(active=my_user).order_by('-last_accessed')

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
       
        current_user.profile.award_points(50)

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
    current_user = request.user
    current_user = User.objects.get(username=current_user)
    profile = Profile.objects.get(user=current_user)
    userbadges = UserBadge.objects.filter(user=current_user)
    # mypoints = Profile.objects.get(user=current_user).points   
    # mylevel = Profile.objects.get(user=current_user).status
    # myrank = Profile.objects.get(user=current_user).rank_status  
    # display_level =  profile.get_status_display()
    # display_rank =  profile.get_rank_status_display()

    # args = {'user': request.user, 'mypoints': mypoints, 'mylevel':mylevel, 'myrank':myrank}
    args = {'user': request.user, 'profile':profile, 'userbadges':userbadges}
    return render(request, 'catalog/profile.html', args)

@login_required
def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your profile has been updated!') 


            # edw badge gia to prwto lvl
            current_user = request.user
            current_user = User.objects.get(username=current_user)
            number = Badges.objects.get(pk=3)
            alreadygiven = UserBadge.objects.filter(user=current_user).filter(badg=number)
            if alreadygiven:
                pass
            else:
                badge = UserBadge(user=current_user, badg=number)
                badge.save()


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
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'catalog/change_password.html', args)


def TestView(request):
    current_user = request.user
    current_user = User.objects.get(username=current_user)
    user = request.POST.get('user')
    award_points(current_user, 50)
    award_points(user, 50)

    return HttpResponse('ok')

    
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class LessonsViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer

class MyCourseViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]

    queryset = MyCourse.objects.all()
    serializer_class = MyCourseSerializer


@api_view(['PUT'])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_exp(request, pk, *args, **kwargs):

    profile = Profile.objects.get(pk=pk)
    user = profile.user
    points = profile.points + 50
    # profile.points = points
    # profile.save()

    if points < 350:
        profile.points = points
        profile.save()
    elif points >= 350:
        status = profile.status
        
        print(status)
        if status == 15:
            remaining = points - 350
            profile.points = remaining
            status = 1
            profile.status = status
            rank = profile.rank_status + 1
            print(rank)

            if rank==2:
                number = Badges.objects.get(pk=5)
                alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
                if alreadygiven:
                    pass
                else:
                    badge = UserBadge(user=user, badg=number)
                    badge.save()
            # elif rank==3:
            #     number = Badges.objects.get(pk=5)
            #     alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
            #     if alreadygiven:
            #         pass
            #     else:
            #         badge = UserBadge(user=user, badg=number)
            #         badge.save()
            # elif rank==4:
            #     number = Badges.objects.get(pk=5)
            #     alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
            #     if alreadygiven:
            #         pass
            #     else:
            #         badge = UserBadge(user=user, badg=number)
            #         badge.save()
            # elif rank==5:
            #     number = Badges.objects.get(pk=5)
            #     alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
            #     if alreadygiven:
            #         pass
            #     else:
            #         badge = UserBadge(user=user, badg=number)
            #         badge.save()
            # elif rank==6:
            #     number = Badges.objects.get(pk=5)
            #     alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
            #     if alreadygiven:
            #         pass
            #     else:
            #         badge = UserBadge(user=user, badg=number)
            #         badge.save()
            # elif rank==7:
            #     number = Badges.objects.get(pk=5)
            #     alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
            #     if alreadygiven:
            #         pass
            #     else:
            #         badge = UserBadge(user=user, badg=number)
            #         badge.save()


            profile.rank_status = rank
            profile.save()

        elif status < 15:
            remaining = points - 350
            profile.points = remaining
            status = status + 1

            if status == 15:
                # edw badge gia ta 15 lvl
                number = Badges.objects.get(pk=6)
                alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
                if alreadygiven:
                    pass
                else:
                    badge = UserBadge(user=user, badg=number)
                    badge.save()

            # edw badge gia to prwto lvl
            number = Badges.objects.get(pk=2)
            alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
            if alreadygiven:
                pass
            else:
                badge = UserBadge(user=user, badg=number)
                badge.save()

        profile.status = status
        profile.save()

# badge gia to prwto lesson
    number = Badges.objects.get(pk=4)
    alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
    if alreadygiven:
        pass
    else:
        badge = UserBadge(user=user, badg=number)
        badge.save()
                

    print(profile.points)
    print("Experience added!")


    return Response({"result":"success"})



@api_view(['PUT'])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def complete_course(request, pk, *args, **kwargs):

    profile = Profile.objects.get(pk=pk)
    user = profile.user
    points = profile.points + 50
    profile.points = points
    profile.save()

    print(profile.points)
    print("Experience added!")


    ccourse = request.data["course"]
    cid = request.data["cid"]
    print(ccourse)
    print(cid)
    # completed_course = MyCourse.objects.get(course=ccourse)
    c_id = Course.objects.get(id=cid)
    status = MyCourse(active=user, course=c_id, status='c')
    status.save()

    print(status.status)

    # edw badge gia complete to ma8hma
    number = Badges.objects.get(pk=1)
    alreadygiven = UserBadge.objects.filter(user=user).filter(badg=number)
    if alreadygiven:
        pass
    else:
        badge = UserBadge(user=user, badg=number)
        badge.save()

    return Response({"result":"success"})
