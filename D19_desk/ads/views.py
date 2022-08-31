from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import User, Post
from .forms import PostForm
from django.http import HttpResponse
from django.core.cache import cache


class AddPostView(CreateView):
    template_name = 'ads/add_post.html'
    form_class = PostForm


class PostsView(ListView):
    model = Post
    template_name = 'ads/posts.html'
    context_object_name = 'posts'


class PostUpdateView(UpdateView):
    template_name = 'ads/add_post.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDetailView(DetailView):
    template_name = 'ads/post_detail.html'
    form_class = PostForm
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj
