from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
  ListView, 
  DetailView,
  CreateView,
  UpdateView,
  DeleteView
)
from .models import Post

# Create your views here.
def home(req):
  context = {
    'posts': Post.objects.all()
  }
  return render(req, 'blog/home.html', context) # This will look for a template in blog/templates/blog/home.html

class PostListView(ListView):
  model = Post
  template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
  context_object_name = 'posts' # This is the variable that will be used in the template
  ordering = ['-date_posted']
  paginate_by = 5
  
class UserPostListView(ListView):
  model = Post
  template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
  context_object_name = 'posts' # This is the variable that will be used in the template
  paginate_by = 5
  
  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted')
    
  
class PostDetailView(DetailView):
  model = Post
  template_name = 'blog/detail.html'
  
class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content']
  
  def form_valid(self, form):
    form.instance.author = self.request.user # Set the author to the current user
    return super().form_valid(form)
  
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']
  
  def form_valid(self, form):
    form.instance.author = self.request.user # Set the author to the current user
    return super().form_valid(form)
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
  
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  success_url = '/'
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False

def about(req):
  return render(req, 'blog/about.html', {'title': 'About'})