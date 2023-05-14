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


