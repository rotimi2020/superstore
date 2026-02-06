# Django Single-App Dashboard Platform

This is a Django-based project that hosts multiple applications under one project.
It includes an analytics dashboards and a custom staff admin panel.

## Apps Included
- Superstore Sales Dashboard
- Custom Staff Admin Dashboard (separate from Django admin)

All apps run within a single Django project using clean URL routing.

--------------------------------------------------

## Features
- User and staff authentication
- Custom staff dashboard 
- Interactive data dashboards
- CRUD operations (including no-page-refresh updates)
- Modular Django app structure


--------------------------------------------------

## Project Structure (Simplified)
```

superstore/
├── superstore/          # Django project settings, main URLs, WSGI/ASGI
├── superstore_app/      # Core application logic
│   ├── static/          # Static files (CSS, JS, images)
│   └── templates/       # HTML templates
├── staff/               # Staff-related app (admin, staff features)
└── manage.py            # Django management script

```



--------------------------------------------------

## Installation & Setup

1. Clone the repository

git clone https://github.com/rotimi2020/superstore.git
cd superstore

2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate
Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Apply database migrations

python manage.py migrate

5. Create a superuser

python manage.py createsuperuser

6. Run the development server

python manage.py runserver

--------------------------------------------------

## Accessing the Application
```

Home: http://127.0.0.1:8000/
Superstore Dashboard: 
Staff Login: /staff/login/
Django Admin: /admin/

```

--------------------------------------------------

## Deployment

The project can be deployed on platforms such as Render, Railway, or a VPS
using Gunicorn and Nginx.

--------------------------------------------------

## License

MIT License
