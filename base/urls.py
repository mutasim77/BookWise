from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    # Main
    path('', main, name='main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('genre/<str:pk>', BookGenreView.as_view(), name='book_genre'),
    
    #Profile 
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/book-add/', UserBookAddView.as_view(), name='user_book_add'),
    path('profile/blog-add/', UserBlogAddView.as_view(), name='user_blog_add'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
