from django.urls import path, include
from rest_framework import routers

from edu.apps import EduConfig
from edu import views

app_name = EduConfig.name

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('lessons/', views.LessonListAPIView.as_view(), name="list-lesson"),
    path('lessons/create/', views.LessonCreateAPIView.as_view(), name="create-lesson"),
    path('lessons/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name="detail-lesson"),
    path('lessons/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name="update-lesson"),
    path('lessons/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name="destroy-lesson"),
    path('', include(router.urls)),
]
