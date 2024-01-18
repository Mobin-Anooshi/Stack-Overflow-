from django.shortcuts import render, redirect
from django.views import View
from account.forms import UserRegistretionForm , UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
# Create your views here.


class UserRegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistretionForm
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
    
class UserLogoutView(View):
    def get(self ,request):
        logout(request)
        messages.success(request , 'you logout is successfully ','success')
        return redirect('home:home')