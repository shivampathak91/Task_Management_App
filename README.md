# Task Management App

A REST API for user registration, login, and managing tasks. It is built with
FastAPI, SQLAlchemy, and Alembic.

## Requirements

- Python 3.10 or newer
- A database supported by SQLAlchemy and its corresponding database driver

## Setup

Create and activate a virtual environment, then install the app's dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic-settings python-dotenv fastapi-mail email-validator PyJWT "pwdlib[argon2]" "psycopg[binary]"
```

Create a `.env` file in the repository root with the required application
settings:

```dotenv
DB_CONNECTION=your-sqlalchemy-database-url
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
EXP_TIME=60
```

Keep `.env` and all real credentials out of Git.

## Run locally

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. FastAPI's interactive API
documentation is at `http://127.0.0.1:8000/docs`.

## Registration email

When a user registers through `POST /user/register`, the app queues a
confirmation email to the address provided. Email is sent through Gmail SMTP
(`smtp.gmail.com`, port `587`, STARTTLS), as configured in
`src/utils/mail.py`.

The mail module currently contains placeholder Gmail settings. Email delivery
will not work until valid SMTP credentials are configured. For Gmail, use a
Google App Password (not your regular account password) and ensure 2-Step
Verification is enabled on the Google account.

**Security note:** The current mail module keeps its SMTP settings in source
code rather than reading them from environment variables. Do not put a real
password or App Password in a file that will be committed or pushed to GitHub.
As currently written, this implementation is not suitable for safely enabling
email on a public deployment without changing the code to load credentials from
private environment variables.

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/user/register` | Register a user |
| `POST` | `/user/login` | Log in and receive a token |
| `GET` | `/user/is_auth` | Check the current user's authentication |
| `POST` | `/tasks/create` | Create a task |
| `GET` | `/tasks/all_tasks` | List tasks |
| `GET` | `/tasks/one_task/{task_id}` | Get a task |
| `PUT` | `/tasks/update_task/{task_id}` | Update a task |
| `DELETE` | `/tasks/delete_task/{task_id}` | Delete a task |

Task endpoints require the token returned by login in the `Authorization`
header, for example: `Authorization: Bearer <token>`.

## Database migrations

Alembic is configured to use the `migrations/` directory. Apply migrations
with:

```powershell
alembic upgrade head
```

The application also calls `Base.metadata.create_all()` at startup.
