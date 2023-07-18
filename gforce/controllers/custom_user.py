import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from gforce.repositories.user import CustomUserRepository
from gforce.helpers.base import SuccessJSONResponse, BadRequestJSONResponse
from gforce.models import Country, City, Countrylanguage
from gforce.repositories.data import DataRepository
from gforce.controllers.data import DataController


class UserController:
    """
    Controller class for managing user-related operations.
    """

    @staticmethod
    @api_view(["POST"])
    def register_user(request):
        """
        Register a new user.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template for successful registration or failure message.

        """
        post_data = request.data
        success, response = CustomUserRepository.create_user(post_data)
        if not success:
            return render(request, "signup_fail.html", {"message": response})
        return render(request, "login.html")

    @staticmethod
    @api_view(["POST"])
    def send_email_otp(request):
        """
        Send OTP to user's email for verification.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template for successful OTP generation or failure message.

        """
        post_data = request.data
        print(post_data)
        email = post_data.get("email")
        success, response = CustomUserRepository.validate_user(email=email)
        if not success:
            return render(request, "send_otp_fail.html", {"message": response})
        otp = "".join([random.choice("0123456789") for i in range(6)])
        subject = "Login OTP for Gforce App"
        from_email = "gforce1310@outlook.com"
        try:
            send_mail(
                subject=subject,
                message=f"Please use this OTP to login: {otp}",
                from_email=from_email,
                recipient_list=[email],
                fail_silently=False,
            )
            success, response = CustomUserRepository.create_otp_record(
                email=email, otp=otp
            )
        except Exception as error:
            print(error.__dict__)
            return render(request, "send_otp_fail.html")
        return render(request, "verify_otp.html")

    @staticmethod
    @api_view(["POST"])
    def verify_otp(request):
        """
        Verify the OTP provided by the user.

        Args:
            request: The HTTP request object.

        Returns:
            A redirect to the home page on successful OTP verification or an error page.

        """
        post_data = request.data
        print(post_data)
        otp = post_data.get("otp")
        success, response = CustomUserRepository.verify_otp(otp=otp)
        if not success:
            return render(request, "invalid_otp.html")
        return redirect(DataController.home_page)

    @staticmethod
    @api_view(["GET"])
    def register_view(request):
        """
        Render the signup HTML template.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template for the signup page.

        """
        return render(request, "signup.html")

    @staticmethod
    @api_view(["GET"])
    def login_view(request):
        """
        Render the login HTML template.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template for the login page.

        """
        return render(request, "login.html")

    @staticmethod
    @api_view(["GET"])
    def verify_otp_view(request):
        """
        Render the verify OTP HTML template.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template for the verify OTP page.

        """
        return render(request, "verify_otp.html")
