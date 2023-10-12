# kwetu-heroku
This is a backend application created and deployed using Heroku service. 
agent details - faithkaburu@gmail.com password-faith

## Features
This app consists of three main routes each route having specific methods related to it.
1. /houses - This route consists of a list of houses with properties of the specific house. Has a GET and POST request where users can add a set of new house listings to the route
2. /houses/:id - This route specifies a specific house related to its id. Has a GET request where it returns a specific dress and a POST request to update a specific part of a house
3. /agents - This route lists a dictionary of agents with their properties. Has a GET request.
4. /agents/:id - This route lists specific agents related by their id. Houses a GET request
5. /users - This route has a GET request to list a dictionary of users
6. /users/:id - This route has a GET request that brings properties related to a specific user by their ID.
7. Signin - This route authenticates already existing users
8. Signup - This route creates new users to the system and authenticates them when carrying out certain requests
9. JWT tokens - Carries out user authentication and authorization

## Usage
Git clone this repository to your local machine and navigate into it. Install the dependencies through the pipfile and run flask run to fire it up locally.
Certain routes are protected and you are needed to have agent privileges to carry out certain functionalities.

## Technologies used
1. Python - To carry out the mapping
2. SQLAlchemy - For the database 
3. Bcrypt - For password hashing and token encryption
4. JWT - For creation of session tokens

## Developers 
1. Prince Hope
2. Emmanuel Peter
3. Faith Kaburu
4. Bitutu Osoro

## License
MIT License



