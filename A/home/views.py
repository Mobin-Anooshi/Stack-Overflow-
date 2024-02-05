from django.shortcuts import render,redirect , get_object_or_404
from django.views import View
from home.models import Post ,Comment,Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from home.forms import PostCreateUpdateForm , CommentCreateForm ,PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class HomeView(View):
    form_class = PostSearchForm
    def get(self , request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        
        return render(request , 'home/index2.html',{'posts':posts,'form':self.form_class})
    

class PostDetailView(View):
    form_class = CommentCreateForm
    
    def setup(self , request , *args, **kwargs):
        self.post_instance = get_object_or_404(Post , pk = kwargs['post_id'] , slug = kwargs['post_slug'])
        return super().setup(request , *args, **kwargs)
        
    def get(self , request , post_id , post_slug):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like= True
        return render(request , 'home/detail.html',{'post':self.post_instance , 'comments':comments , 'form':self.form_class,'can_like':can_like})


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
    form_class = PostCreateUpdateForm

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
    form_class = PostCreateUpdateForm
    def get(self , request ):
        form = self.form_class
        return render(request ,'home/create.html',{'form':form})
        
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.slug = slugify(form.cleaned_data['body'][:30])
            new_form.save()
            messages.success(request , 'you created new post ','success')
            return redirect('home:post_detail' , new_form.id , new_form.slug)
        
        
# poae hvie cjrh amvc
class UserCommentsView(LoginRequiredMixin,View):
    form_class = CommentCreateForm
    def get(self , request , *args, **kwargs):
        form = self.form_class
        return render(request , 'home/comment.html' ,{'form':form})
    def post(self , request , *args, **kwargs):
        form = self.form_class(request.POST)
        post = Post.objects.get(pk= kwargs['post_id'])
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request , 'comment posted','success')
            return redirect('home:post_detail' ,post.id , post.slug)
        messages.error('you cant comment this post')
        return redirect('home:home')
        
class UserReplyCommentView(LoginRequiredMixin, View):
    form_class = CommentCreateForm
    def get(self,request , *args, **kwargs):    
        form = self.form_class
        return render(request , 'home/replycomment.html',{'form':form})
    def post(self ,request , *args, **kwargs):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post , pk =kwargs['post_id'])
        comment = get_object_or_404(Comment , pk=kwargs['comment_id'])
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply=True
            reply.save()
            messages.success(request,'successfull','success')
            return redirect('home:post_detail' ,post.id , post.slug)
        messages.error('you cant comment this post')
        return redirect('home:home')       

class UserPostLikeView(LoginRequiredMixin ,View):
    def get(self , request ,*args, **kwargs):
        post = get_object_or_404(Post ,pk=kwargs['post_id'])
        like = Vote.objects.filter(user=request.user , post=post)
        if like.exists() :
            messages.success(request , 'you dislike this post','danger')
            like.delete()        
        else:
            Vote.objects.create(user=request.user , post=post)
            messages.success(request , 'you liked this post','success')
        return redirect('home:post_detail',post.id,post.slug)
