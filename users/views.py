from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView
from users.forms import LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
 
class LoginView(TemplateView):
    http_method_names = ['get', 'post']

    template_name = "users/login.html"
    def get_context_data(self, **kwargs):
        form = LoginForm()
        context = super(LoginView,self).get_context_data(**kwargs)
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.add_message(request, messages.SUCCESS, "You successfully authenticated!")
            return redirect('/')
        
        context = super(LoginView,self).get_context_data(**kwargs)
        context['form'] = form
        return render (request, self.template_name, {
            'form': form,
        })   
       

class RegisterView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = "users/signup.html"
    
    def get_context_data(self, **kwargs):
        form = LoginForm()
        context = super(LoginView,self).get_context_data(**kwargs)
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.add_message(request, messages.SUCCESS, "You successfully authenticated!")
            return redirect('/')
        
        context = super(LoginView,self).get_context_data(**kwargs)
        context['form'] = form
        return render (request, self.template_name, {
            'form': form,
        })   


class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView,self).get_context_data(**kwargs)
        context["user"] = {
            'login':'saucesamba',
            'email':'saucesamba@vk.com',
            'nickname':'MR. Sauce',
        }
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView,self).dispatch(request, *args, **kwargs)
    

@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')


class LogOutView(TemplateView):
    pass