from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "users/login.html"

class RegisterView(TemplateView):
    template_name = "users/signup.html"

class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView,self).get_context_data(**kwargs)
        context[""] = []
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView,self).dispatch(request, *args, **kwargs)
    