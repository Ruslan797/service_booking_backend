# Service Booking Backend API

Backend REST API for a service booking platform.

This project demonstrates the development of a backend service where users can browse services and create bookings.  
It was created as a study project to practice backend architecture, REST API development, authentication, and Docker deployment.

---

## Features

- User registration and authentication
- JWT authentication
- Service listing
- Create bookings
- View bookings
- Role-based access
- REST API architecture

---

## Technologies

- Python
- Django
- Django REST Framework
- SQLite / PostgreSQL
- Docker
- Docker Compose
- JWT Authentication

---

## Project Structure


apps/
├── accounts
├── bookings
├── payments

core/


---

## Installation

Clone repository

git clone https://github.com/Ruslan797/service_booking_backend.git

Go to project folder

cd service_booking_backend

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Run server

python manage.py runserver

API will be available at

http://127.0.0.1:8000

---

## Author

Ruslan Buievskyi  
Python Backend Developer
