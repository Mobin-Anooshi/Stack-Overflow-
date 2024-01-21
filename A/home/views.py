from django.shortcuts import render,redirect
from django.views import View
from home.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from home.forms import PostUpdateForm
from django.utils.text import slugify
# Create your views here.


class HomeView(View):
    def get(self , request):
        posts = Post.objects.all()
        return render(request , 'home/index.html',{'posts':posts})
    

class PostDetailView(View):
    def get(self , request , post_id , post_slug):
        post  =Post.objects.get(pk = post_id , slug=post_slug)
        return render(request , 'home/detail.html',{'post':post})


class PostDeleteView(LoginRequiredMixin , View):
    def get(self , request , post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request , 'post deleted','success')
        else :
            messages.error(request ,'you cant delete this post','danger')
        return redirect('home:home')
    

class PostUpdateView(LoginRequiredMixin , View):
    form_class = PostUpdateForm

    def setup(self,request ,*args, **kwargs):
        self.post_instanse = Post.objects.get(pk= kwargs['post_id'])
        return super().setup(request ,*args, **kwargs)
    
    def dispatch(self , request ,*args, **kwargs):
        post = self.post_instanse
        if not post.user.id == request.user.id :
            messages.error(request , 'you cant update this post','danger')
            return redirect('home:home')
        return super().dispatch(request , *args, **kwargs)
    def get(self ,request, *args, **kwargs):
        post = self.post_instanse
        form = self.form_class(instance=post)
        return render(request , 'home/update.html', {'form':form})

    def post(self , request , *args, **kwargs):
        post = self.post_instanse
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data['body'][:30])
            new_form.save()
            messages.success(request, 'post updated', 'success')
            return redirect('home:post_detail',post.id , post.slug)
        
class PostCreateView(LoginRequiredMixin , View):
    def get(self , request ):
        pass
    def get(self , request):
        pass 