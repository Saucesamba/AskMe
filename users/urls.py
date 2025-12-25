from django.urls import path

from users.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name = "login"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name = "profile"),
    path('logout/', logout_view, name = "logout"),
]