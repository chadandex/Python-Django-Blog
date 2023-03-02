from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# Old function based homepage view
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    # -= Home Page =-
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    # -= Blog Post Details =-
    # post_detail.html
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    # -= Create Blog Post =-
    # post_form.html
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # auto set author to current user on post creation
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # -= Update Blog Post =-
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # auto set author to current user on blog post creation
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # make sure author editing is the actual author of blog post
        post = self.get_object()  # grab post we are trying to update
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # -= Blog Post Details =-
    # post_confirm_delete.html
    model = Post
    success_url = '/'

    def test_func(self):
        # make sure author deleting is the actual author of blog post
        post = self.get_object()  # grab post we are trying to delete
        if self.request.user == post.author:
            return True
        return False


def about(request):
    # -= About Blog Page =-
    return render(request, 'blog/about.html', {'title': 'About'})
