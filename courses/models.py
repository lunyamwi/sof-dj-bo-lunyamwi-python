from django.db import models
from django.urls import reverse
from students.models import Membership
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description=models.TextField()
    allowed_memberships=models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail',kwargs={'slug':self.slug})

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')

    @property
    def articles(self):
        return self.article_set.all().order_by('pub_date')


class Lesson(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=120)
    course=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    position=models.IntegerField()
    video_url=models.CharField(max_length=200)
    thumbnail=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail',
        kwargs={
            'course_slug':self.course.slug,
            'lesson_slug':self.slug
        })



class Article(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=200)
    course=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    lesson=models.ForeignKey(Lesson,on_delete=models.SET_NULL,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    content=RichTextUploadingField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:article-detail',
        kwargs={
            'course_slug':self.course.slug,
            'article_slug':self.slug
        })
