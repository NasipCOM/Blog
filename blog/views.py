from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import View
from .forms import PostForm   
from django.urls import reverse  

# Create your views here.
def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts':posts})


# def post_detail(request, slug):
#     return render(request, 'blog/post_detail.html', context={'post':post})

class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_create_form.html', context={'form':form})
    
    
    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_create_form.html', context={'form':bound_form})

class PostUpdate(View):
    def get(self, request, slug):
        post = Post.objects.get(slug__iexact= slug)
        bound_form = PostForm(instance = post)
        return render(request, 'blog/post_update_form.html', context={'form':bound_form, 'post':post})

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact = slug)
        bound_form = PostForm(request.POST, instance = post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_update_form', context={'form':bound_form, 'post':post})    

class PostDelete(View):
    def get(self, request,slug):
        post = Post.objects.get(slug__iexact=slug)
        return render(request, 'blog/post_delete_form.html', context={'post':post})
    
    
    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        post.delete()
        return redirect(reverse('posts_list_url'))     

class PostDetail(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug__iexact=slug)
        return render(request, 'blog/post_detail.html', context={'post':post, 'admin_object':post, 'detail':True})

