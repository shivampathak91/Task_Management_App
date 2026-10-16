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

Keep `.env` and all real credentials out of Git. Registration attempts to send a
confirmation email using the SMTP settings in `src/utils/mail.py`. That module
currently does not read its credentials from environment variables; do not add
real passwords or app-passwords to tracked source files.

## Run locally

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. FastAPI's interactive API
documentation is at `http://127.0.0.1:8000/docs`.

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
