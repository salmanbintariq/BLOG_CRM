from django.urls import path
from .views import home, blog_detail, write_blog
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('write-blog/', write_blog, name='write_blog'),
    path('blog-detail/<int:id>/',blog_detail, name='blog-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)