# kwetu-heroku
This is a backend application created and deployed using Heroku service.

## Features
This app consists of three main routes each route having specific methods related to it.
1. /houses - This route consists of a list of houses with properties of the specific house. Has a GET and POST request where users can add a set of new house listings to the route
2. /houses/:id - This route specifies a specific house related to its id. Has a GET request where it returns a specific dress and a POST request to update a specific part of a house
3. /agents - This route lists a dictionary of agents with their properties. Has a GET request.
4. /agents/:id - This route lists specific agents related by their id. Houses a GET request
5. /clients - This route has a GET request to list a dictionary of users
6. /clients/:id - This route has a GET request that brings properties related to a specific user by their ID.

## Usage
Git clone this repository to your local machine and navigate into it. Install the dependencies through the pipfile and run flask run to fire it up locally.

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



