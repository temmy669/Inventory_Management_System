# Inventory Management System API

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Interaction](#api-interacion)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Hosting](#hosting-instructions)

## Introduction

This is a RESTful API for an Inventory Management System that allows users to manage products, categories, and inventory levels efficiently. This project is built using Django and provides a robust backend for handling inventory data.

## Technologies Used

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Docker 
- Git

## Features

- CRUD operations for products, suppliers and inventory
- Inventory management
- Docker support for easy deployment
- Detailed API documentation

## Setup Instructions

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.x installed
- PostgreSQL installed and running
- Git installed
- Docker installed 

### 1. Clone the Repository

```bash
git clone git@github.com:temmy669/InventoryApp.git
cd Inventory
```
### 2. Create and Activate a Virtual Environment

Create a virtual environment and activate it.

#### On Windows:
- **Create**: 
  ```bash
  python3 -m venv venv
  ```
- **Activate**:
  ```bash
  venv/scripts/activate
  ```
#### On MacOS:
- **Create**:
  ```bash
  python3 -m venv venv
  ```
- **Activate**:
  ```bash
  venv/bin/activate
  ```
### 3. Install Dependencies

Install the necessary dependencies listed in the `requirements.txt` file using the command `pip install -r requirements.txt`.  

### 4. Configure Enviroment Variables

Create a `.env` file in the root directory of the project and add your environment variables. For example:
```
SECRET_KEY='your-secret-key'
DATABASE_NAME='your-database-name'
DATABASE_USER='your-database-user'
DATABASE_PASSWORD='your-database-password'
DATABASE_HOST='your-database-host'
DATABASE_PORT='your-database-port'

```

### 5. Run Migrations

Apply database migrations to set up your database schema.
#### On Windows:
- **Make Migrations**: 
  ```bash
  python manage.py makemigrations
  ```
- **Migrate**: 
  ```bash
  python manage.py migrate
  ```
  
#### On Linux/MacOS:
- **Make Migrations**: 
  ```bash
  python3 manage.py makemigration
  ```
#### On Linux/MacOS:
- **Migrate**: 
  ```bash
  python3 manage.py migrate
  ```
  

### 6. Create Superuser

To access the admin panel, create a superuser account.
To create the superuser account use the command `python manage.py createsuperuser`, after you would be required to input your email, user, name and password to be able to access the admin panel.

### 7. Run the development server

Start the development server to run your API.

Your API should now be accessible at `http://127.0.0.1:8000/`


## API Interaction

You can use tools like Postman or curl to interact with and test the API endpoints.

## API Endpoints

The following endpoints are available in the Inventory Management System API:

| Endpoint                          | Method      | Description                                             | 
|-----------------------------------|-------------|---------------------------------------------------------|
| `/api/v1/products/`               | GET         | List all products with pagination and filtering options. |
| `/api/v1/products/`               | POST        | Add a new product (name, description, price, supplier). | 
| `/api/v1/products/{id}/`          | PUT         | Update product details.                                 | 
| `/api/v1/products/{id}/`          | DELETE      | Remove a product.                                     | 
| `/api/v1/suppliers/`              | GET         | List all suppliers.                                    |
| `/api/v1/suppliers/`              | POST        | Add a new supplier (name, contact info).              | 
| `/api/v1/suppliers/{id}/`         | PUT         | Update supplier details.                               |
| `/api/v1/suppliers/{id}/`         | DELETE      | Remove a supplier.                                    | 
| `/api/v1/inventory/`              | GET         | Check inventory levels for each product.              | 
| `/api/v1/inventory/`              | POST        | Update inventory levels (product ID, quantity).       | 
| `/api/v1/inventory/generate-inventory-report/`| POST | To generate inventory reports                     |
| `/api/v1/inventory/generate-supplier-report/`| POST | To generate supplier performance reports            |
| `/api/v1/notifications/`           |  GET    |   To list the otifications                                 |  

### Full API documentation can be found at `http://127.0.0.1:8000/swagger/`
Ensure that the Django server is running

## Testing

This project includes tests to ensure the functionality and reliability of the Inventory Management System API.

### Running Tests
To run the test use the command `python manage.py appname.test`
  replace appname with the name of the application in the project you want to test.

## Hosting Instructions

To access the endpoints on the live application, please follow these steps:

1. **Base URL**  
   The application is hosted at:  
   [https://inventory-management-system-nmrq.onrender.com](https://inventory-management-system-nmrq.onrender.com)

2. **Accessing Endpoints**  
   Since the base URL ([https://inventory-management-system-nmrq.onrender.com](https://inventory-management-system-nmrq.onrender.com)) does not display specific content on its own, append endpoint paths to view specific functionalities. For example:
   - **Admin Panel**:  
     [https://inventory-management-system-nmrq.onrender.com/admin](https://inventory-management-system-nmrq.onrender.com/admin)  
     _(Admin credentials are required for access)_

   - **API Endpoints**:  
     Append specific API paths after `/api/`, such as:  
     [https://inventory-management-system-nmrq.onrender.com/api/v1/products/](https://inventory-management-system-nmrq.onrender.com/api/v1/products/)

3. **Sample Endpoint Access**  
   To access the "products" endpoint in your API, use the following URL:  
   [https://inventory-management-system-nmrq.onrender.com/api/v1/products/](https://inventory-management-system-nmrq.onrender.com/api/v1/products/)

4. **Further Instructions**  
   For other pages or actions, simply append the corresponding endpoint path to the base URL.


