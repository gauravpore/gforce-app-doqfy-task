from django.db.models import Q
from gforce.models import Country, City, Countrylanguage
from gforce.repositories.base import BaseRepository
from gforce.serializers.base import CountrySerializer


class DataRepository:
    """
    A repository class for retrieving data from the database.
    """
    @staticmethod
    def get_autosuggest_data():
        """
        Retrieve autosuggest data for countries, cities, and languages.

        Returns:
            A tuple indicating the success status and a dictionary containing the autosuggest data.

        """
        country_data = Country.objects.all()
        city_data = City.objects.all()
        language_data = Countrylanguage.objects.all()
        data = {
            "countries": country_data,
            "cities": city_data,
            "languages": language_data,
        }
        return True, data

    @staticmethod
    def get_search_result_data(querylist):
        """
        Get search results based on the provided query list.

        Args:
            querylist (list): A list of queries to search for.

        Returns:
            A tuple indicating the success status and a string containing the HTML content of the search results.

        """
        # Perform database queries or other logic to retrieve relevant information
        results = []
        for query in querylist:
            # Example: Search for cities, countries, and languages
            cities = City.objects.filter(
                Q(name__icontains=query) | Q(district__icontains=query)
            )
            countries = Country.objects.filter(
                Q(name__icontains=query) | Q(continent__icontains=query)
            )
            languages = Countrylanguage.objects.filter(language__icontains=query)

            # Process the results and create the HTML content to be displayed
            for city in cities:
                results.append(
                    f'<p>{city.name} - <a href="/country-details?country_code={city.countrycode.code}" target="_blank">{city.countrycode.name}--{city.name}</a></p>'
                )
            for country in countries:
                results.append(
                    f'<p><a href="/country-details?country_code={country.code}" target="_blank">{country.name}--{country.continent}</a></p>'
                )
            for language in languages:
                results.append(f"<p>{language.language}</p>")

        output = "".join(results)
        print(output)
        return True, output

    @staticmethod
    def get_country_details(country_code):
        """
        Get detailed information about a country based on the provided country code.

        Args:
            country_code (str): The country code.

        Returns:
            A tuple indicating the success status and the serialized data of the country.

        """
        country_data = Country.objects.filter(code=country_code).first()
        if not country_data:
            return False, "Invalid country code"
        serialized_data = CountrySerializer(country_data).data
        return True, serialized_data
