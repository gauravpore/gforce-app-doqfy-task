from django.urls import path

from .views import UserController, DataController

urlpatterns = [
    path("login-page/", UserController.login_view, name="login-page"),
    path("signup-page/", UserController.register_view, name="signup-page"),
    path("signup-user/", UserController.register_user, name="signup-new-user"),
    path("send-otp-email/", UserController.send_email_otp, name="send-otp-email"),
    path("verify-otp-page/", UserController.verify_otp_view, name="verify-otp-page"),
    path("verify-otp/", UserController.verify_otp, name="verify-otp"),
    path("home-page/", DataController.home_page, name="home-page"),
    path("search-results/", DataController.search_results, name="search-results"),
    path("country-details/", DataController.get_country_details, name="country-details"),
]
