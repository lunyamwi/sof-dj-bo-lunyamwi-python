from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView,View
from .models import Course,Lesson,Article
from students.models import UserMembership,Membership




# Create your views here.
class CourseCreateView(CreateView):
    model = Course
    fields=['slug','title','description','allowed_memberships',]
    success_url=reverse_lazy('courses:list')

class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course

class LessonCreateView(CreateView):
    model = Lesson
    fields=['slug','title','course','position','video_url','thumbnail',]
    success_url=reverse_lazy('courses:list')

class LessonDetailView(View):

    def get(self,request,course_slug,lesson_slug,*args,**kwargs):
        
        course = Course.objects.filter(slug=course_slug).first()
        lesson = Lesson.objects.filter(slug=lesson_slug)
        # import pdb;pdb.set_trace()
        user_membership = UserMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership.membership.membership_type
        
        course_allowed_mem_types = course.allowed_memberships.all()

        context={
            'object':None
        }        

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context={'object':lesson}

        return render(request,"courses/lesson_detail.html",context)

class ArticleCreateView(CreateView):
    model = Article
    fields=["slug","title","lesson","course","content"]
    success_url=reverse_lazy('courses:article-list')



class ArticleListView(ListView):
    model = Article


class ArticleDetailView(View):

        def get(self,request,course_slug,article_slug,*args,**kwargs):

            course = Course.objects.filter(slug=course_slug).first()
            article = Article.objects.filter(slug=article_slug)
            print(article)
            
            # import pdb;pdb.set_trace()
            
            user_membership = UserMembership.objects.filter(user=request.user).first()
            user_membership_type = user_membership.membership.membership_type
            
            course_allowed_mem_types = course.allowed_memberships.all()

            context={
                'object':None
            }        

            if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
                context={'object':article}

            return render(request,"courses/article_detail.html",context)