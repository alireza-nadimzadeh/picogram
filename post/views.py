from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from .forms import NewCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class ExploreListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = ['-created_date']
    template_name = "post/explore.html"
    context_object_name = 'posts'

    paginate_by = 15


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-created_date']
    paginate_by = 15

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(
            author__in=self.request.user.profile.following.all())
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-created_date')
        data['comments'] = comments_connected

        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post=self.get_object())
        new_comment.save()
        this_post = self.get_object()
        post_id = this_post.id
        return redirect(f'/post/{post_id}')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
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


@login_required
def like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    post.likes.add(user)
    return redirect('post-detail', pk=pk)


@login_required
def unlike(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    post.likes.remove(user)
    return redirect('post-detail', pk=pk)
