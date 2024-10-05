# Inventory Management System
## About
A backend API that supports CRUD operations on inventory items built using django rest framework.
## Functionalities & Features
* CRUD operation on inventory items
* APIs built using DRF
* Error handling is done through validations
* Data Serialization
* Cache Implementation
* Loggers implementation
* Test cases using unittest and django test framework
* JWT Authentication of each API
## Tech Stack
* Python
* DRF
* MySQL
* Redis
* Python
## Setup Instructions
* create a folder and download this code inside that folder
* install python (version used 3.11.8)
* create virtual environment (e.g., python -m venv venv)
* activate virtual environment (venv/Scripts/activate.bat)
* install requirements (pip install -r requirements.txt)
* install Redis in your machine (references are mentioned in settings.py)
* install and configure MySQL in your machine (references are mentioned in settings.py)
* create a database "inventory" using MySQL Workbench (create database inventory;)
* start the server (python manage.py runserver)
## API Documentation
* There are 3 APIs used in this application to perform CRUD operations.
* inventory-manager/items/ :- it will create item in the inventory database (POST)
* inventory-manager/items/{item_id}/ :- it will fetch the item details (GET)
* inventory-manager/items/{item_id}/ :- it will update the item details (PUT)
* inventory-manager/items/{item_id}/:- it will delete the item from the database (DELETE)
* inventory-manager/get_jwt_token/:- it will fetch JWT token (POST)
* username and password you can use: tanmaya, admin to generate the access token and pass the access token in the header request
## Usage Guide
* after the setup is successful, run the server and use tool like Postman to trigger the APIs.
* download Postman: https://www.postman.com/downloads/?utm_source=postman-home
* hit the endpoint: inventory-manager/get_jwt_token/ to get the access token usig the payload (or you can create you own users): 
{
    "username": "tanmaya",
    "password": "admin"
}
* NOTE:- pass the generated token in the headers of each API through Postman > Authorization > select Bearer token
* to add an item to the inventory, use the endpoint: localhost:8000/inventory-manager/items/ and payload structure: 
{
    "name":"Rice",
    "description": "Staple food of India",
    "stock_count": 15
}
* similary to fetch the details of the item use the endpoint: localhost:8000/inventory-manager/items/{item_id}/
* item_id is the id of the item that you can check from the DB in MySQL Workbench.
* similarly, the PUT method can be used using the payload structure of POST to update any item.
* DELETE method can be used to delete the item from the Database using the endpoint mentioned in the API Documentation section.
* to run the test cases, use the command: python manage.py test inventory.tests (NOTE: Authentication is not included in test cases my bad! so before running the test cases, please comment out Authentications in all the APIs)
## References and Sources
* download Postman: https://www.postman.com/downloads/?utm_source=postman-home
* download MySQL: https://dev.mysql.com/downloads/installer/
* follow this to configure MySQL: https://www.w3schools.com/mysql/mysql_install_windows.asp
* install Redis cache: github.com/microsoftarchive/redis/release (download the .msi file)
* a video demo for the project: https://screenrec.com/share/dvYzfKPo94

Tada! you are done with your implementation for a backend API setup using Django Rest Framework. Keep Learning.
For queries, drop me an email: tanmayanayak1305@gmail.com
