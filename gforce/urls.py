from django.urls import path

from .views import UserController


urlpatterns = [
    path("signup-user", UserController.register_user, name="signup-new-user"),
    path("send-otp-email", UserController.send_email, name="send-otp-email"),
]
