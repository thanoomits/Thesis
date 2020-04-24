from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('teachers/', views.PostedbyListView.as_view(), name='teachers'),
    path('teacher/<int:pk>', views.PostedbyDetailView.as_view(), name='teacher-detail'),
]