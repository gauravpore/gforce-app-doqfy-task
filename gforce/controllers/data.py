import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from gforce.helpers.base import SuccessJSONResponse, BadRequestJSONResponse
from gforce.models import Country, City, Countrylanguage
from gforce.repositories.data import DataRepository
from gforce.repositories.user import CustomUserRepository


class DataController:
    """
    A controller class for handling data-related operations.
    """

    @staticmethod
    @api_view(["GET"])
    def home_page(request):
        """
        Render the home page.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template with autosuggest data.

        """
        # Render the HTML template
        success, response = DataRepository.get_autosuggest_data()
        return render(request, "home.html", response)

    @staticmethod
    @api_view(["GET"])
    def search_results(request):
        """
        Get search results based on the provided query.

        Args:
            request: The HTTP request object.

        Returns:
            A JSON response containing the search results.

        """
        query = request.GET.get("query", "")
        querylist = query.split(",")
        print(querylist)
        success, response = DataRepository.get_search_result_data(querylist=querylist)
        return SuccessJSONResponse(response)



    @staticmethod
    @api_view(["GET"])
    def get_country_details(request):
        """
        Get detailed information about a country.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template with the country details.

        """
        country_code = request.GET.get("country_code")
        success, response = DataRepository.get_country_details(
            country_code=country_code
        )
        if not success:
            return render(request, 'country_error.html', {'message': response})
        return render(request, "country_page.html", {'country': response})
