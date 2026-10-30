# CodeAlpha Event Registration System

A REST API built with Django and Django REST Framework that allows users to create and manage events, view event details, and handle attendee registrations.

## Features

- Create, view, update, and delete events.
- Register attendees for events.
- View all registrations or filter registrations by event.
- View individual registration details.
- Cancel existing registrations.
- Validate attendee email addresses.
- Prevent duplicate registrations for the same event and email.
- Enforce event capacity limits.
- View the number of registered attendees for each event.
- Manage events and registrations through the Django Admin dashboard.
- Automatically reset browsable API forms after successful submissions.
- Six automated API tests.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- REST API

## Project Structure

```text
CodeAlpha_EventRegistration/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── event_api/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/pchauhan24-dev/CodeAlpha_EventRegistration.git
cd CodeAlpha_EventRegistration
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

http://127.0.0.1:8000/

Django Admin dashboard:

http://127.0.0.1:8000/admin/

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | List all events |
| POST | `/api/events/` | Create an event |
| GET | `/api/events/<id>/` | Retrieve event details |
| PUT | `/api/events/<id>/` | Update an event |
| PATCH | `/api/events/<id>/` | Partially update an event |
| DELETE | `/api/events/<id>/` | Delete an event |
| GET | `/api/registrations/` | List all registrations |
| POST | `/api/registrations/` | Register an attendee |
| GET | `/api/registrations/<id>/` | Retrieve registration details |
| DELETE | `/api/registrations/<id>/` | Cancel a registration |
| GET | `/api/registrations/?event=<id>` | Filter registrations by event |

## Example: Create an Event

Send a POST request to `/api/events/` with the following JSON:

```json
{
    "name": "Python Workshop",
    "description": "A beginner-friendly Python workshop",
    "date": "2027-01-15T10:00:00+05:30",
    "location": "Raipur",
    "capacity": 50
}
```

## Example: Register an Attendee

Send a POST request to `/api/registrations/` with the following JSON:

```json
{
    "event": 1,
    "attendee_name": "Test User",
    "attendee_email": "testuser@example.com"
}
```

Replace `1` with an existing event ID.

## Run Automated Tests

Run the following command:

```bash
python manage.py test event_api
```

The project includes six automated tests covering:

- Event listing.
- Event creation.
- Attendee registration.
- Duplicate registration prevention.
- Invalid email validation.
- Event capacity validation.

## Database

The project uses SQLite as its default database. Django creates the database file when migrations are applied.

## Internship Project

Developed as part of the **CodeAlpha Backend Development Internship**.

## License

This project is intended for educational and internship purposes.
