# E-Commerce REST API (Django + DRF)

## Project Overview
A full-featured e-commerce backend with:
- User Authentication (JWT)
- Product Management
- Cart + Orders
- Admin Dashboard & Stats
- Docker + Postgres
- Pytest unit tests

##  Tech Stack
- Python 3.11
- Django + Django REST Framework
- PostgreSQL
- JWT Auth (`djangorestframework-simplejwt`)
- Docker, Docker Compose
- Pytest

## Setup Instructions

```bash
git clone <repo-url>
cd ecommerce
cp .env.example .env
docker-compose build
docker-compose up
