from django.db.models import QuerySet
from gforce.models import CustomUser, Otp

from gforce.repositories.base import BaseRepository


class CustomUserRepository(BaseRepository):
    def __init__(
        self,
        *args,
        item: CustomUser = None,
        many: bool = False,
        item_list: QuerySet = None,
        **kwargs,
    ):
        super(CustomUserRepository, self).__init__(
            *args, model=CustomUser, item=item, many=many, item_list=item_list, **kwargs
        )

    @staticmethod
    def create_user(user_data: dict):
        """
        Registers/Creates a new user.
        Params:
            validated_data -> validated form data from the incoming request
        Returns:
            (CustomUser or success, message)
        """
        mobile_number = user_data.get("mobile_number")
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")
        gender = user_data.get("gender")
        if not email or not first_name:
            return False, "Invalid params"
        user = CustomUser.objects.filter(email=email, mobile_number=mobile_number)
        if user:
            return False, "User already exists with provided email or mobile number"
        user = CustomUser.objects.create(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
        )
        user.save()
        return True, user

    @staticmethod
    def create_otp_record(email, otp):
        """
        Registers/Creates a new user.
        Params:
            validated_data -> validated form data from the incoming request
        Returns:
            (CustomUser or success, message)
        """
        otp_record = Otp.objects.filter(email=email).first()
        if otp_record:
            otp_record.otp = otp
            otp_record.save()
        else:
            otp_record = Otp.objects.create(email=email, otp=otp)
            otp_record.save()
        return True, otp_record

    @staticmethod
    def verify_otp(email, otp):
        """
        Registers/Creates a new user.
        Params:
            validated_data -> validated form data from the incoming request
        Returns:
            (CustomUser or success, message)
        """
        otp_record = Otp.objects.filter(email=email, otp=otp)
        if otp_record:
            return True, "Otp verified successfully"
        return False, "Invalid Otp"
