from django.urls import path
from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("registration/", views.registration_user, name="registration"),
    path("otp_varification/", views.otp_varification, name="otp"),
    path("update_profile/", views.update_profile, name="update_profile")
]
