# Binebil Backend

Django REST API backend for Dolmuş Takip Sistemi (Public Transport Tracking System).

## 🚀 Features

- RESTful API for routes, schedules, fares, and authentication
- KML file upload for route data
- Role-based permissions and token authentication

## 🛠️ Tech Stack

- Django & Django REST Framework
- SQLite (default, can use PostgreSQL/MySQL)
- Python 3.8+

## 📦 Quick Start

```bash
cd binebilBackend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API: `http://localhost:8000`

## 🏗️ Structure

```
binebilBackend/
├── api/            # Main API app (models, views, urls, permissions)
├── binebilBackend/ # Project settings
├── media/          # Uploaded KML files
└── manage.py
```

## 🌐 API Overview

- `POST /api/login/` – Login
- `GET/POST /api/routes/` – List/Create routes
- `GET/PUT/DELETE /api/routes/{id}/` – Route detail/update/delete
- `GET/POST /api/schedules/` – List/Create schedules
- `GET/POST /api/fares/` – List/Create fares

## 🔒 Auth & Permissions

- Token-based authentication
- Custom permissions for route owners
- Most endpoints require login

## ⚙️ Config

**Database**: Edit `settings.py` for PostgreSQL/MySQL if needed.

**CORS**: Allow frontend origins in `CORS_ALLOWED_ORIGINS`.

**Env Vars**: Create `.env` for secrets:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🤝 Contributing

- Follow Django standards
- Write tests and migrations
- Update API docs

## 📄 License

Part of Dolmuş Takip Sistemi.
