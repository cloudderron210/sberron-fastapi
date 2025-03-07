# Sberron bank app


## Description
This project is a Python-based web application built with FastAPI. It provides a RESTful API for managing bank operations, including:  
• User registration using JWT  
• Managing accounts  
• Transactions  
• Card management  
It is designed to be lightweight, scalable, and easy to deploy.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/cloudderron210/sberron-fastapi.git
   cd sberron-fastapi
   ```
   
2.  Create .env file:

    • Copy the .env.template file to .env:
    ```bash
    cp .env.template .env

    ```
    • Open the .env file and fill in the required values:

    ```env
    # Database Configuration
    DATABASE_URL=postgresql://user:password@db:5432/dbname

    # JWT Configuration
    JWT_SECRET_KEY=your_jwt_secret_key

    # Other Settings
    DEBUG=true
    ```
    
3. Start the application:
    
   ```bash
   sudo docker compose up --build
   ```
   
4. The API will be available at http://localhost:8000.
   
---

## Technologies Used
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL** 
- **Docker** 



    


