from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('courses.urls',namespace='courses')),
    path('user/', include('django.contrib.auth.urls')),
    path('memberships/',include('students.urls',namespace='members')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('articles/',include('articles.urls')),
]
if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)



