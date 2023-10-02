from django.urls import path
from .views import LessonsList, LessonList, LessonStatisticsList

urlpatterns = [
    path('', LessonsList.as_view(), name='lessons-list'),
    path('<int:id>/', LessonList.as_view(), name='lesson-list'),
    path('statistics/', LessonStatisticsList.as_view(), name='statistics-list')
]