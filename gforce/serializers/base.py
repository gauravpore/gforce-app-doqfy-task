from rest_framework import serializers
from gforce.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "code",
            "name",
            "continent",
            "region",
            "surfacearea",
            "indepyear",
            "population",
            "lifeexpectancy",
            "gnp",
            "gnpold",
            "localname",
            "governmentform",
            "headofstate",
            "capital",
            "code2",
        )
