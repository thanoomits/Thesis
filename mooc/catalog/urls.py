from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:pk>/lessons', views.LessonsListView.as_view(), name='lesson'),
    path('lessons/<int:pk>', views.LessonsDetailView.as_view(), name='lesson-detail'),
    path('course/<int:pk>/addtolist', views.addtolist, name='add-course-to-list'),
    path('course/<int:pk>/deletefromlist', views.deletefromlist, name='delete-course-from-list'),
    path('teachers/', views.PostedbyListView.as_view(), name='teachers'),
    path('teacher/<int:pk>', views.PostedbyDetailView.as_view(), name='teacher-detail'),
    path('teacher/create', views.PostedbyCreate.as_view(), name='teacher-create'),
    path('teacher/<int:pk>/update', views.PostedbyUpdate.as_view(), name='teacher-update'),
    path('teacher/<int:pk>/delete', views.PostedbyDelete.as_view(), name='teacher-delete'),
    path('mycourses/', views.ActiveCoursesByUserListView.as_view(), name='my-active'),
    path('profile/', views.view_profile, name='view-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('change-password/', views.change_password, name='change-password'),
] 