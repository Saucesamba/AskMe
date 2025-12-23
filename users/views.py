from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from users.forms import LoginForm, SignUpForm, ProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.utils.decorators import method_decorator

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
       

class SignUpView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = "users/signup.html"

    def get_context_data(self, **kwargs):
        form = SignUpForm()
        context = super(SignUpView,self).get_context_data(**kwargs)
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "You have successfully registered!")
            return redirect('index')
        
        context = super(SignUpView,self).get_context_data(**kwargs)
        context['form'] = form
        return render (request, self.template_name, {
            'form': form,
        })   

@method_decorator(login_required, name = 'dispatch')    
class ProfileView(TemplateView):
    template_name = "users/profile.html"
    http_method_names = ['get', 'post']

    def get_form(self, user=None):
        if user:
            return ProfileForm(instance=user)
        return ProfileForm()
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView,self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = self.get_form(self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user  
        )
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile') 
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
    

    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView,self).dispatch(request, *args, **kwargs)
    

@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')