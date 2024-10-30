# Django Live Chat

A real-time chat application built with Django and WebSockets. This project allows users to communicate in real-time, making it suitable for various applications such as customer support, community forums, or personal messaging.

## Features

- Real-time messaging using Django Channels
- User authentication
- Chat rooms for group conversations
- User-friendly interface

## Requirements

Before running this project, ensure you have the following installed:

- **Python 3.x**
- **Node.js** (for managing frontend assets)
- **Django 3.x or higher**
- **Django Channels**

## Required Packages

To install the required Python packages, you can use `pip`. Create a virtual environment and install the dependencies as follows:

1. Clone the repository:
   ```bash
   git clone https://github.com/HjtDev/django-live-chat.git
   cd django-live-chat
   ```
   
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
   
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Install Node.js packages (if applicable):
   ```bash
   npm install
   ```
   
## Setup

Configure your database: Update the database settings in settings.py according to your database configuration.

1. Run migrations:
   ```bash
   python manage.py makemigrations && python manage.py migrate
   ```
   
2. Create superuser(to see all the rooms as admin):
   ```bash
   python manage.py createsuperuser
   ```
   
3. Run the development server:
   ```bash
   python manage.py runserver
   ```

