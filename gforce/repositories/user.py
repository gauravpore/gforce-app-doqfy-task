from django.db.models import QuerySet
from gforce.models import CustomUser, Otp
from gforce.repositories.base import BaseRepository


class CustomUserRepository(BaseRepository):
    """
    Repository class for managing custom user data.
    """
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

        Args:
            user_data (dict): Validated form data from the incoming request.

        Returns:
            Union[bool, tuple]: A tuple indicating the success status and either the created user object or an error message.
        """
        mobile_number = user_data.get("mobile")
        first_name = user_data.get("fname")
        last_name = user_data.get("lname")
        email = user_data.get("email")
        gender = user_data.get("gender")
        if type(email) == list:
            first_name = first_name[0]
            last_name = last_name[0]
            email = email[0]
            mobile_number = mobile_number[0]
            gender = gender[0]
        if not email or not first_name:
            return False, "Invalid params"
        user = CustomUser.objects.filter(email=email)
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
        Creates an OTP record for the user.

        Args:
            email (str): Email address of the user.
            otp (str): One-Time Password generated for the user.

        Returns:
            Union[bool, tuple]: A tuple indicating the success status and either the created OTP record object or an error message.
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
    def verify_otp(otp):
        """
        Verifies the provided OTP.

        Args:
            otp (str): One-Time Password to be verified.

        Returns:
            Union[bool, tuple]: A tuple indicating the success status and either a success message or an error message.
        """
        otp_record = Otp.objects.filter(otp=otp)
        if otp_record:
            return True, "Otp verified successfully"
        return False, "Invalid Otp"

    @staticmethod
    def validate_user(email):
        """
        Validates a user based on the provided email address.

        Args:
            email (str): Email address of the user.

        Returns:
            Union[bool, tuple]: A tuple indicating the success status and either a success message or an error message.
        """
        user = CustomUser.objects.filter(email=email)
        if not user:
            return False, "User not found"
        return True, "User validated successfully"
