import random
from rest_framework.decorators import api_view


from gforce.repositories.user import CustomUserRepository
from gforce.helpers.base import (
    SuccessJSONResponse,
    BadRequestJSONResponse,
)
from django.core.mail import send_mail


class UserController:
    @staticmethod
    @api_view(["POST"])
    def register_user(request):
        """
        For registering new user
        """
        post_data = request.data
        success, response = CustomUserRepository.create_user(post_data)
        if not success:
            return BadRequestJSONResponse(message=response)
        return SuccessJSONResponse(message="User registered successfully")

    # @staticmethod
    # @api_view(["POST"])
    # def login_user(request):
    #     post_data = request.data
    #     mobile_number = post_data.get("mobile_number")
    #     password = post_data.get("password")
    #     if not mobile_number or not password:
    #         return BadRequestJSONResponse(message="Inavlid Post data")
    #     user = get_or_none(CustomUser, mobile_number=mobile_number, is_active=True)
    #     if not user:
    #         return NotFoundJSONResponse(message="User not found")
    #     if user.password != str(password):
    #         return UnauthorizedJSONResponse("Invalid Credentials")
    #     if not user.is_active:
    #         return ForbiddenJSONResponse("User has been deactivated")
    #     return SuccessJSONResponse(tokens)

    # @staticmethod
    # @api_view(["POST"])
    # @login_required
    # def logout_user(request):
    #     # TODO: Need to fix below functionality
    #     token = get_access_token(request)
    #     access_token = AccessToken(token)
    #     cache_expire = datetime_from_epoch(access_token.get("exp")) - timezone.now()
    #     cache.set(token, True, timeout=cache_expire.seconds)
    #     return SuccessJSONResponse(request.META)

    @staticmethod
    @api_view(["POST"])
    def send_email(request):
        post_data = request.data
        email = post_data.get("email")
        otp = "".join([random.choice("0123456789") for i in range(6)])
        subject = "Login OTP for Gforce App"
        from_email = "gforce1310@outlook.com"
        try:
            send_mail(
                subject=subject,
                message=f"Please use this otp to login: {otp}",
                from_email=from_email,
                recipient_list=[email],
                fail_silently=False,
            )
            success, response = CustomUserRepository.create_otp_record(
                email=email, otp=otp
            )
        except Exception as error:
            print(error.__dict__)
            return BadRequestJSONResponse(message=error)
        return SuccessJSONResponse(message="OTP Email sent successfully")

    @staticmethod
    @api_view(["POST"])
    def verify_otp(request):
        post_data = request.data
        otp = post_data.get("otp")
        email = post_data.get("email")
        success, response = CustomUserRepository.verify_otp(email=email, otp=otp)
        if not success:
            return BadRequestJSONResponse(message=response)
        return SuccessJSONResponse(message=response)
