# CodeAlpha Event Registration System

A REST API built with Django and Django REST Framework that allows users to create events, view event details, and manage event registrations.

## Features

- Create, view, update, and delete events.
- Register attendees for events.
- View all registrations or filter registrations by event.
- Cancel an existing registration.
- Validate attendee email addresses.
- Prevent duplicate registrations for the same event and email.
- Enforce event capacity limits.
- View the number of registered attendees for each event.
- Automated API tests.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- REST API

## Project Structure

```text
event_registration/
├── config/
│   ├── settings.py
│   └── urls.py
├── event_api/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_EventRegistration.git
cd CodeAlpha_EventRegistration
```

### 2. Create and activate a virtual environment

Windows PowerShell:

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

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

http://127.0.0.1:8000/

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | List all events |
| POST | `/api/events/` | Create an event |
| GET | `/api/events/<id>/` | Retrieve an event |
| PUT | `/api/events/<id>/` | Update an event |
| DELETE | `/api/events/<id>/` | Delete an event |
| GET | `/api/registrations/` | List registrations |
| POST | `/api/registrations/` | Register an attendee |
| DELETE | `/api/registrations/<id>/` | Cancel a registration |
| GET | `/api/registrations/?event=<id>` | Filter registrations by event |

## Example: Create an Event

Send a POST request to `/api/events/` with JSON:

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

Send a POST request to `/api/registrations/` with JSON:

```json
{
  "event": 1,
  "attendee_name": "Test User",
  "attendee_email": "testuser@example.com"
}
```

Replace `1` with an existing event ID.

## Run Automated Tests

```bash
python manage.py test event_api
```

The project currently includes six automated tests covering event creation, event listing, attendee registration, duplicate registration prevention, invalid email validation, and event capacity limits.

## Database

The project uses SQLite by default. Django creates the database file when migrations are applied.

## Internship Project

Developed as part of the CodeAlpha Backend Development Internship.

## License

This project is intended for educational and internship purposes.

