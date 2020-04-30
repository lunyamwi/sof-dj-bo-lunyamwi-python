from django.urls import path
from .views import (
    ArticleDetailView,
    ArticleListView,
    ArticleCreateView,
    CourseCreateView,
    CourseListView,
    CourseDetailView,
    LessonCreateView,
    LessonDetailView,
)

app_name='courses'

urlpatterns=[
    # path('',IndexView,name='home'),
    path('',CourseListView.as_view(),name='list'),
    path('<slug>',CourseDetailView.as_view(),name='detail'),
    path('courses/<course_slug>/<lesson_slug>',LessonDetailView.as_view(),name='lesson-detail'),
    path('course/create/',CourseCreateView.as_view(),name='course-create'),
    path('lesson/create/',LessonCreateView.as_view(),name='lesson-create'),
    path('article/create/',ArticleCreateView.as_view(),name='article-create'),
    path('article/list/',ArticleListView.as_view(),name='article-list'),
    path('<course_slug>/<article_slug>',ArticleDetailView.as_view(),name='article-detail'),
]