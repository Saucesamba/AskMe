from django.urls import path

from users.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name = "login"),
    path('signup/', RegisterView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name = "profile"),
    path('logout/', LogOutView.as_view(), name = "logout"),
]