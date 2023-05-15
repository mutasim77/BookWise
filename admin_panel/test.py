from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

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
    
    #
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User

def validate_form_data(username, password, confirm_password, age, gender):
    errors = {}
    
    # Empty fields
    if not (username and password and confirm_password and age and gender):
        errors['empty_fields'] = 'All fields are required!'

    # Less than 8 characters password error(register)
    if len(password) < 8:
        errors['short_password'] = 'Password should have at least 8 characters!'

    # Minimum one upper case and one lower case and one number should contain password
    if not (re.search('[a-z]', password) and re.search('[A-Z]', password) and re.search('[0-9]', password)):
        errors['weak_password'] = 'Password should contain at least one upper case letter, one lower case letter, and one number!'

    # Check if passwords match
    if password != confirm_password:
        errors['password_mismatch'] = 'Passwords do not match!'

    #  Username shouldn’t be duplicated.
    user = User.objects.filter(username=username)
    if user:
        errors['existing_username'] = 'Username already exists!'

    return errors


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from hashlib import sha256
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.db.models import Count
from django.db.models import Q
from django.views import View
from django.views.generic.edit import CreateView
from .models import *
from .utils import validate_form_data
from admin_panel.models import AddNewBook
import os
import sys
from .forms import * 


#? REGISTER USER
class RegisterView(View):
    def get(self, request):
        response = render(request, 'base/register.html')
        response['Cache-Control'] = 'no-cache'
        return response
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        password_hash = sha256(password.encode()).hexdigest()
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # Validate form data
        errors = validate_form_data(username, password, confirm_password, age, gender)
        if errors:
            error_message = list(errors.values())[-1]
            messages.add_message(request, messages.ERROR, error_message)
            return redirect('register')

        obj = User()
        obj.username = username
        obj.password = password_hash
        obj.age = age
        obj.gender = gender
        obj.save()
        messages.success(request, 'Registration successful!')
        return redirect('login_user')

# ? LOGIN USER
class LoginUserView(View):
    def get(self, request):
        context = {}
        return render(request, 'base/login.html', context)
    
    def post(self, request):
        context = {}
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            password_hash = sha256(password.encode()).hexdigest()
            data = User.objects.get(username=username, password=password_hash)
            
            if data is not None:
                request.session['data_id'] = data.id
                return redirect(reverse('main'))
            
        except Exception as e:
            context['error'] = "Invalid username or password"

        return render(request, 'base/login.html', context)


#*----------Profile User----------

# ? PROFILE
class ProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return render(request, 'base/profile.html', {'user': user})
    
# ? Edit user info
class ProfileEditView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return render(request, 'base/profile_edit.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        user.username = request.POST.get('username')
        user.age = request.POST.get('age')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.fullname = request.POST.get('fullname')
        
        hash_password = sha256((request.POST.get('password')).encode()).hexdigest() 
        user.password = hash_password
        
        image_file = request.FILES.get('image')
        if image_file:
            if user.image:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(user.image)))
            user.image = image_file
            
        user.save()
        return redirect('profile', pk=pk)
    
# ? User Add Book
class UserBookAddView(CreateView):
    model = Book
    form_class = AddNewBook
    template_name = 'base/user_add_book.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.is_published = False
        return super().form_valid(form)
    
# # ? User Add Book
class UserBlogAddView(CreateView):
    model = Blog
    form_class = AddNewBlog
    template_name = 'base/user_add_blog.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        return super().form_valid(form)
    
#? Logout User
class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login_user')

    
#*----------Views----------

#? Book genres
class BookGenreView(View):
    def get(self, request, pk):
        context = {}
        books = Book.objects.filter(genre__icontains=pk)
        context['books'] = books
        context['genre_name'] = pk
        return render(request, 'base/genres.html', context)
    
#? Blog
class BlogView(View):
    def get(self, request):
        blogs = Blog.objects.all()
        return render(request, 'base/blog.html', {'blogs' : blogs})

#? Contact
class ContactView(View):
    def get(self, request):
        return render(request, 'base/contact.html')
        
#? MAIN   
def main(request):
    context = {}
    data_id = request.session.get('data_id')
    if data_id is not None:
        data = User.objects.get(id=data_id)
        context['data'] = data

    #all books
    books = Book.objects.filter(is_published=True)
    context['books'] = books
    
    #best author books
    best_author = Book.objects.filter(author='Khaled Hosseini')
    context['best_author'] = best_author

    #best author books
    upcomings = Book.objects.all().order_by('-id')[:4:1]
    context['upcomings'] = upcomings 
      
    #genre list
    genre_list = sorted(Book.objects.values('genre').annotate(num_books=Count('id')), key=lambda x: x['genre'])
    context['genre_list'] = genre_list
        
    search_input = request.GET.get('search') or ''
    search_results = Book.objects.none()
    last_viewed = Book.objects.none()
    
    # seach-area;
    if search_input:
        search_results = Book.objects.filter(title__icontains=search_input)
        context['books'] = search_results
        context['flag'] = 'Flag'
        
        search_history = request.session.get('search_history', [])
        if search_history:
            last_viewed = Book.objects.filter(title__icontains=search_history[-1])
            
        search_history.append(search_input)
        search_history = search_history[-5:]
        request.session['search_history'] = search_history
    
    context['last_viewed'] = last_viewed

    return render(request, 'base/main.html', context)

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'age', 'gender']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        if not any(char.islower() for char in password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        age = cleaned_data.get('age')
        gender = cleaned_data.get('gender')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(_("Passwords don't match."))
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('This username is already taken.'))
        
        
        
        
class AddNewBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'publisher', 'description', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'autocomplete': 'off'}),
            'publisher': forms.TextInput(attrs={'placeholder': 'Your Name', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'placeholder': 'description', 'min': '1', 'autocomplete': 'off'}),
        }



class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, help_text="Enter your desired username", widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    password = forms.CharField(max_length=50, help_text="Enter a strong password", widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'autocomplete': 'off'}))
    confirm_password = forms.CharField(max_length=50, help_text="Confirm your password",
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    age = forms.IntegerField(help_text="Enter your age", widget=forms.NumberInput(
        attrs={'placeholder': 'Enter age', 'min': '1'}))
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect, help_text="Select your gender")
    
    from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    is_active = models.BooleanField(default=False)
    
    # additionally
    image = models.ImageField(upload_to='users/', null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=70, help_text="The title of the book.")
    image = models.ImageField(upload_to='images/')
    rating = models.IntegerField(help_text="The the reviewer has given.")
    author = models.CharField(max_length=70, help_text="The name of Author")
    price = models.CharField(max_length=10, help_text="Price of book")
    is_published = models.BooleanField(default=False)
    genre = models.CharField(null=True,max_length=70, help_text="The genre of the book.")
    description = models.TextField(help_text="A detailed description of the book.", null=True)
    pages = models.IntegerField(help_text="The number of pages in the book.", null=True)
    publisher = models.CharField(max_length=100, help_text="The publisher of the book.", null=True)
    publish_date = models.DateField(help_text="The publication date of the book.", null=True)
    language = models.CharField(max_length=50, help_text="The language of the book.", null=True)
    book_type = models.CharField(max_length=50, help_text="The type of the book.", null=True)
   
    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=150, help_text="The title of the blog")
    date = models.DateField(auto_now_add=True)
    publisher = models.CharField(max_length=100, help_text="The publisher of the blog", null=True)
    description = models.TextField(help_text="A description of the blog", null=True)
    image = models.ImageField(upload_to='blogs/')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.views import View

from base.models import User, Book


#*-----------User-----------

#? Edit user info
class UserEditView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'admin_panel/user/user_edit.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.username = request.POST.get('username')
        user.age = request.POST.get('age')
        user.phone = request.POST.get('phone')
        user.email = request.POST.get('email')
        user.fullname = request.POST.get('fullname')
        user.save()
        return redirect('user_list')
  
#? Delete User from table
class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'admin_panel/user/user_delete.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list')
    
# ? List of all users;
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'admin_panel/user/user_list.html', {'users' : users})
    
    
# ? List of all blogs;
class BlogListView(View):
    def get(self, request):
        blogs = Blog.objects.all()
        return render(request, 'admin_panel/blog/blogs_list.html', {'blogs' : blogs})

#*-----------Book-----------

# ? Edit user info
class BookEditView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'admin_panel/book/book_edit.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.image = request.POST.get('image')
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.rating = request.POST.get('rating')
        book.price = request.POST.get('price')
        book.genre = request.POST.get('genre')
        book.is_published = request.POST.get('is_published', False) == "on"
        book.save()
        return redirect('book_list')

# ? Delete Book from table
class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'admin_panel/book/book_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('book_list')

# ? Add Book to the table
class BookAddView(View):
    def get(self, request):
        form = AddNewBook()
        return render(request, 'admin_panel/book/add_new_book.html', {'form': form})

    def post(self, request):
        form = AddNewBook(request.POST, request.FILES) 
        if form.is_valid():
            new_book = Book(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                rating=form.cleaned_data['rating'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image'],
                genre=form.cleaned_data['genre'],
                is_published = request.POST.get('is_published', False) == "on",
            )
            new_book.save()
            return redirect('book_list')
        return render(request, 'admin_panel/book/add_new_book.html', {'form': form})

# ? List of all Books;
class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'admin_panel/book/book_list.html', {'books': books})


#*-----------BLOG-----------

# ? Edit user info
class BlogEditView(View):
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        return render(request, 'admin_panel/blog/blog_edit.html', {'blog': blog})

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        blog.title = request.POST.get('title')
        blog.publisher = request.POST.get('publisher')
        blog.description = request.POST.get('description')
        
        blog.save()
        return redirect('blog_list')

# ? Delete Book from table
class BlogDeleteView(View):
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        return render(request, 'admin_panel/blog/blog_delete.html', {'blog': blog})

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        blog.delete()
        return redirect('blogs_list')
    
    
#*-----------ADMIN-----------

# ? Admin login
class AdminLoginView(View):
    def get(self, request):
        error_message = ''
        return render(request, 'admin_panel/admin_login.html', {'error_message': error_message})
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/admin/users/')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'admin_panel/admin_login.html', {'error_message': error_message})
      
# ? Admin logout
class AdminLogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('admin_login')



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
