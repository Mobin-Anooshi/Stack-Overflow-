from django.shortcuts import render
from django.views import View
from account.forms import UserRegistretionForm
# Create your views here.


class UserRegisterView(View):
    def get(self , request):
        form = UserRegistretionForm()
        return render(request , 'account/register.html',{'form':form})
    def post(self , request):
        pass