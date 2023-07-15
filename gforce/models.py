import random

from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Create your models here.
# CUSTOM USER MANAGER
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given mobile_number and password.
        """
        if not email:
            raise ValueError(_("The mobile_number must be set"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given mobile_number and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


def generate_user_id():
    user_id = "".join(
        [random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVXYZ") for i in range(10)]
    )
    return user_id


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user Model --> stores user information in respective fields
    """

    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    user_id = models.CharField(
        max_length=10, default=generate_user_id, unique=True, null=True
    )
    mobile_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=gender_choices, default="Male")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    remark = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)


class City(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    name = models.CharField(
        db_column="Name", max_length=35
    )  # Field name made lowercase.
    countrycode = models.ForeignKey(
        "Country", models.DO_NOTHING, db_column="CountryCode"
    )  # Field name made lowercase.
    district = models.CharField(
        db_column="District", max_length=20
    )  # Field name made lowercase.
    population = models.IntegerField(
        db_column="Population"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "city"


class Country(models.Model):
    code = models.CharField(
        db_column="Code", primary_key=True, max_length=3
    )  # Field name made lowercase.
    name = models.CharField(
        db_column="Name", max_length=52
    )  # Field name made lowercase.
    continent = models.CharField(
        db_column="Continent", max_length=13
    )  # Field name made lowercase.
    region = models.CharField(
        db_column="Region", max_length=26
    )  # Field name made lowercase.
    surfacearea = models.FloatField(
        db_column="SurfaceArea"
    )  # Field name made lowercase.
    indepyear = models.SmallIntegerField(
        db_column="IndepYear", blank=True, null=True
    )  # Field name made lowercase.
    population = models.IntegerField(
        db_column="Population"
    )  # Field name made lowercase.
    lifeexpectancy = models.FloatField(
        db_column="LifeExpectancy", blank=True, null=True
    )  # Field name made lowercase.
    gnp = models.FloatField(
        db_column="GNP", blank=True, null=True
    )  # Field name made lowercase.
    gnpold = models.FloatField(
        db_column="GNPOld", blank=True, null=True
    )  # Field name made lowercase.
    localname = models.CharField(
        db_column="LocalName", max_length=45
    )  # Field name made lowercase.
    governmentform = models.CharField(
        db_column="GovernmentForm", max_length=45
    )  # Field name made lowercase.
    headofstate = models.CharField(
        db_column="HeadOfState", max_length=60, blank=True, null=True
    )  # Field name made lowercase.
    capital = models.IntegerField(
        db_column="Capital", blank=True, null=True
    )  # Field name made lowercase.
    code2 = models.CharField(
        db_column="Code2", max_length=2
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "country"


class Countrylanguage(models.Model):
    countrycode = models.OneToOneField(
        Country, models.DO_NOTHING, db_column="CountryCode", primary_key=True
    )  # Field name made lowercase. The composite primary key (CountryCode, Language) found, that is not supported. The first column is selected.
    language = models.CharField(
        db_column="Language", max_length=30
    )  # Field name made lowercase.
    isofficial = models.CharField(
        db_column="IsOfficial", max_length=1
    )  # Field name made lowercase.
    percentage = models.FloatField(db_column="Percentage")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "countrylanguage"
        unique_together = (("countrycode", "language"),)


class Otp(models.Model):
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    otp = models.CharField(max_length=6)
    created_date = CreationDateTimeField()
    updated_date = ModificationDateTimeField(null=True)

    def __str__(self):
        return str(self.email)
