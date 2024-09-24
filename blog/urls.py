from django.urls import path
from .views import home, dashboard,blog_detail, write_blog, category_blogs, edit_blog, delete_blog
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('dashboard/', dashboard, name='dashboard'),
    path('write-blog/', write_blog, name='write_blog'),
    path('blog-detail/<slug:slug>/',blog_detail, name='blog-detail'),
    path('category/<slug:slug>/', category_blogs, name='category_blogs'),

    path('blog/edit/<slug:slug>/', edit_blog, name='edit_blog'),
    path('blog/delete/<slug:slug>/', delete_blog, name='delete_blog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)