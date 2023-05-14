from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    # Admin and User
    path('admin/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/', AdminLogoutView.as_view(), name='admin_logout'),
    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/user-edit/<int:pk>', UserEditView.as_view(), name='user_edit'),
    path('admin/user-delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    
    # Book
    path('admin/books/', BookListView.as_view(), name='book_list'),
    path('admin/book-add', BookAddView.as_view(), name='book_add'),
    path('admin/book-edit/<int:pk>', BookEditView.as_view(), name='book_edit'),
    path('admin/book-delete/<int:pk>', BookDeleteView.as_view(), name='book_delete'),

    # Blogs
    path('admin/blogs/', BlogListView.as_view(), name='blog_list'),
    path('admin/blog-edit/<int:pk>', BlogEditView.as_view(), name='blog_edit'),
    path('admin/blog-delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
