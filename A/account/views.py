from django.shortcuts import render, redirect
from django.views import View
from account.forms import UserRegistretionForm , UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from home.models import Post
from django.urls import reverse_lazy
from account.models import Relation
# Create your views here.


class UserRegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistretionForm

    def dispatch(self , request , *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request , *args, **kwargs)

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name,{'form':form})
    

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request , 'you register successfully','success')
            return redirect('home:home')
        else:
            return render(request , self.template_name,{'form':form})
        
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'


    def dispatch(self , request , *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request , *args, **kwargs)
    def get(self , request):
        form = self.form_class
        return render(request , self.template_name , {'form':form})
    
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username=cd['username'] , password=cd['password'])
            if user is not None:
                login(request , user)
                messages.success(request , 'you login is successfully ','success')
                return redirect('home:home')
            messages.error(request , 'username or password is wrong','warning')
        return render(request , self.template_name , {'form':form})
    
class UserLogoutView(LoginRequiredMixin,View):
    def get(self ,request):
        logout(request)
        messages.success(request , 'you logout is successfully ','success')
        return redirect('home:home')
    

class UserProfileView(LoginRequiredMixin,View):
    def get(self , request , user_id):
        is_following = False
        user = User.objects.get(pk = user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            is_following = True
        return render(request , 'account/profile.html',{'user':user,'posts':posts,'is_following':is_following})
    

class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='account/password_reset_complete.html'



class UserFollowingView(LoginRequiredMixin , View):
    def get(self , request , user_id):
        user = User.objects.get(pk = user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user=user)
        if relation.exists():
            messages.error(request , 'you cant follow this user' , 'danger')
        else:
            Relation.objects.create(from_user = request.user , to_user=user)
            messages.success(request , 'follow' , 'success')
        return redirect('account:user_profile',user.id)  


class UserUnfollowView(LoginRequiredMixin , View):
    def get(self , request , user_id):
        user = User.objects.get(pk = user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request , 'Unfollow','success')
        else :
            messages.error(request , 'you not follow this user')

        return redirect('account:user_profile',user.id)
