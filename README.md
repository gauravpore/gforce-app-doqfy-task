# gforce-app-doqfy-task

# Features

* User signup: Users can create a new account by providing their first name, last name, gender, email, and phone number.
* OTP-based login: When a user attempts to log in, an OTP is sent to their registered email or phone number. The user must provide the correct OTP to authenticate.
* Logout: Users can securely log out of their accounts, which clears their session and redirects them to the login page.
* Dashboard: Upon successful login, users are presented with a dashboard displaying a search bar and a search button.
* Autosuggest: As users start typing in the search bar, the system provides autosuggestions based on available cities, countries, or languages.
* Search results: After pressing the search button, a list of relevant information related to the search query is displayed on a new screen.
* Country details: Whenever the name of a country appears, it is clickable and redirects users to a "Country Details" page, which provides in-depth information about the selected country.

## Technologies Used
* Django: Web framework for building the application.
* Django Rest Framework (DRF): Used for creating API endpoints.
* HTML/CSS: Front-end markup and styling.
* JavaScript/jQuery: Used for handling client-side interactions.
* MySQL: Utilizes a SQL database to store user data and populate information about cities, countries, and languages.
* Postman: API Testing application for testing endpoints.

## Installations and Setup

* Clone the repository:
 ```bash 
git clone <repository-url> 
```
* Create and activate a virtual environment (optional): 
```
python3 -m venv env 
```
```
source env/bin/activate
```
* Install the project dependencies: 
``` 
pip install -r requirements.txt
```
* Run database migrations: 
```
python manage.py migrate
```
* Start the development server:
```
python manage.py runserver
```
Access the application in your browser at http://localhost:8000/

## API Endpoints
```
POST /signup/: Create a new user account.
POST /send-otp-email/: Sends 6-digit otp to user's email for login purpose.
POST /verify-otp/: Validates user entered 6-digit otp to authenticate the user.
GET /search-results/: Returns entire Country, City & CountryLanguage data to feed autosuggest search feature on dashboard.
GET /country-details/: Returns serialized country data from database based on country_code to display on country-details page.
```
