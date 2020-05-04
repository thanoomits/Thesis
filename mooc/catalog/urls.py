from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('teachers/', views.UserListView.as_view(), name='users'),
    path('teacher/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('teacher/create', views.PostedbyCreate.as_view(), name='teacher-create'),
    path('teacher/<int:pk>/update', views.PostedbyUpdate.as_view(), name='teacher-update'),
    path('teacher/<int:pk>/delete', views.PostedbyDelete.as_view(), name='teacher-delete'),
    path('mycourses/', views.ActiveCoursesByUserListView.as_view(), name='my-active'),
]