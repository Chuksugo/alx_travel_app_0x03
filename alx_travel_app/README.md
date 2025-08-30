# ALX Travel App 0x00

A simple Django project for managing travel listings, bookings, and reviews. Includes models, serializers, and a database seeder to populate sample data.

## Features

* **Listings**: Manage travel properties.
* **Bookings**: Record user bookings for listings.
* **Reviews**: Add user reviews for listings.
* **Database Seeder**: Populate the database with sample listings.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Chuksugo/alx_travel_app_0x00.git
cd alx_travel_app_0x00/alx_travel_app
```

2. Create a virtual environment and activate it.
3. Install dependencies:

```bash
pip install -r requirement.txt
```

4. Create a `.env` file in the inner `alx_travel_app` folder with your `SECRET_KEY` and MySQL database credentials.

## Database

Run migrations to create tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

Seed the database with sample listings:

```bash
python manage.py seed
```

## Usage

Open the Django shell to query data:

```bash
python manage.py shell
```

```python
from listings.models import Listing
list(Listing.objects.values_list('title', flat=True))
```
# ALX Travel App API

## Features
- CRUD for Listings
- CRUD for Bookings
- Swagger API Documentation

## Setup
```bash
git clone https://github.com/Chuksugo/alx_travel_app_0x01.git
cd alx_travel_app_0x01
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Payment Integration with Chapa API
This project integrates the Chapa payment gateway for handling bookings.


### Endpoints
- `POST /payment/initiate/` → Initiates payment
- `GET /payment/verify/?tx_ref=<id>` → Verifies payment

### Testing
Use Chapa's sandbox environment.

