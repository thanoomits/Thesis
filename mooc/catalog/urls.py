from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'points', views.ProfileViewSet)
router.register(r'lessons', views.LessonsViewSet)
router.register(r'mycourse', views.MyCourseViewSet)

urlpatterns = [
    path('router/', include(router.urls)),
    path('points/<int:pk>', views.get_exp),
    path('cocourse/<int:pk>', views.complete_course),
    path('', views.index, name='index'),
    path('about/', views.about, name='about-page'),
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