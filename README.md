# CampusOS

A centralized student & department management platform for colleges. Consolidates notices, assignments, departments, and user management into a single role-based system.

Built with **FastAPI** (backend) + **React** (frontend) + **PostgreSQL** (database).

---

## Features

### Role-Based Access (5 Roles)
- **Admin** — System management, user CRUD, department CRUD
- **Principal** — College-wide oversight, HOD management
- **HOD** — Department management, faculty/student management
- **Faculty** — Notice and assignment creation, student management
- **Student** — Read-only access to notices and assignments

### Core Features
- JWT authentication with bcrypt password hashing
- Auto-generated temporary passwords for new users
- Department-scoped visibility (users see their own department)
- Author-only edit/delete for notices and assignments
- "All Departments" notices for Admin/Principal
- In-app notification system with unread count
- Full-text search across notices and assignments
- Role-based dashboards
- Dark mode support
- Responsive mobile layout

---

## Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Core language |
| FastAPI | REST API framework |
| SQLAlchemy 2.0 | ORM |
| PostgreSQL 15 | Database |
| Alembic | Database migrations |
| Pydantic v2 | Data validation |
| python-jose | JWT tokens |
| passlib[bcrypt] | Password hashing |
| Pytest | Testing |

### Frontend
| Technology | Purpose |
|-----------|---------|
| React 18 | UI framework |
| Vite | Build tool |
| Tailwind CSS | Styling |
| React Router | Client-side routing |
| Axios | HTTP client |
| React Hot Toast | Toast notifications |
| Lucide React | Icons |

---

## Project Structure

```
campusos/
├── src/
│   ├── backend/
│   │   ├── alembic/                    # Database migrations
│   │   │   ├── versions/
│   │   │   └── env.py
│   │   ├── app/
│   │   │   ├── api/v1/                 # API routes
│   │   │   ├── core/                   # Config, DB, security
│   │   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── services/               # Business logic
│   │   │   ├── repositories/           # Data access
│   │   │   ├── utils/                  # Helpers
│   │   │   ├── main.py                 # App entry
│   │   │   └── middleware.py           # Logging middleware
│   │   ├── tests/                      # Pytest tests
│   │   ├── alembic.ini
│   │   ├── requirements.txt
│   │   └── .env.example
│   │
│   └── frontend/
│       ├── src/
│       │   ├── components/             # Reusable UI
│       │   ├── pages/                  # Route pages
│       │   ├── services/               # API clients
│       │   ├── context/                # Auth context
│       │   ├── hooks/                  # Custom hooks
│       │   ├── utils/                  # Helpers
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── package.json
│       ├── tailwind.config.js
│       ├── vite.config.js
│       └── .env.example
│
├── .gitignore
└── README.md
```

---

## Setup Instructions

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** and **npm**
- **PostgreSQL 15+**

### Backend Setup

**1. Navigate to backend:**
```bash
cd src/backend
```

**2. Create virtual environment:**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up PostgreSQL:**
```bash
# Login to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE campusos;
CREATE USER campusos_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE campusos TO campusos_user;

# Connect to the database
\c campusos
GRANT ALL ON SCHEMA public TO campusos_user;
ALTER SCHEMA public OWNER TO campusos_user;

# Exit
\q
```

**5. Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

**6. Run migrations:**
```bash
alembic upgrade head
```

**7. Start the server:**
```bash
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**
Swagger docs: **http://localhost:8000/docs**

### Frontend Setup

**1. Navigate to frontend:**
```bash
cd src/frontend
```

**2. Install dependencies:**
```bash
npm install
```

**3. Configure environment:**
```bash
cp .env.example .env
# Default: VITE_API_URL=http://localhost:8000/api/v1
```

**4. Start the dev server:**
```bash
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## Demo Accounts

**Create demo users by running the seed script** (see below) OR create them manually through the Admin dashboard.

Default password for all demo accounts: `demo123`

| Role | Email |
|------|-------|
| Admin | admin@campos.app |
| Principal | principal@gtu.ac.in |
| HOD (CE) | hod.ce@gtu.ac.in |
| HOD (IT) | hod.it@gtu.ac.in |
| HOD (ME) | hod.me@gtu.ac.in |
| Faculty (CE) | mehta.faculty@gtu.ac.in |
| Student (CE) | priya.student@gtu.ac.in |

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Student self-registration |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/me` | Current user profile |
| POST | `/api/v1/auth/change-password` | Change password |

### Users
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/users/` | Admin, Principal, HOD, Faculty |
| POST | `/api/v1/users/` | Admin, Principal, HOD, Faculty |
| GET | `/api/v1/users/me` | All authenticated |
| GET | `/api/v1/users/{id}` | Role-based |
| PUT | `/api/v1/users/{id}` | Role-based |
| DELETE | `/api/v1/users/{id}` | Role-based (higher can delete lower) |
| GET | `/api/v1/users/search?q=` | Role-based |

### Departments
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/departments/` | All authenticated |
| POST | `/api/v1/departments/` | Admin, Principal |
| PUT | `/api/v1/departments/{id}` | Admin, Principal |
| DELETE | `/api/v1/departments/{id}` | Admin, Principal |

### Notices
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/notices/` | All authenticated |
| POST | `/api/v1/notices/` | Admin, Principal, HOD, Faculty |
| GET | `/api/v1/notices/my` | Own notices |
| PUT | `/api/v1/notices/{id}` | Author only |
| DELETE | `/api/v1/notices/{id}` | Author only |

### Assignments
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/assignments/` | All authenticated |
| POST | `/api/v1/assignments/` | Faculty only |
| PUT | `/api/v1/assignments/{id}` | Author only |
| DELETE | `/api/v1/assignments/{id}` | Author only |

### Notifications
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/notifications/` | Own notifications |
| GET | `/api/v1/notifications/unread/count` | Unread count |
| PATCH | `/api/v1/notifications/{id}/read` | Mark as read |

Full API documentation available at `/docs` (Swagger UI) when running in debug mode.

---

## Database Schema

### Users
Stores all user accounts across 5 roles. Fields: `id`, `email`, `hashed_password`, `full_name`, `role`, `department_id`, `is_active`, `must_change_password`, `phone`, `gender`, `date_of_birth`, `profile_picture`, `created_at`, `updated_at`.

### Departments
Academic departments. Fields: `id`, `name`, `code`, `hod_id`, `created_at`.

### Notices
Department announcements. Fields: `id`, `title`, `content`, `department_id` (nullable for "all departments"), `faculty_id`, `is_published`, `created_at`, `updated_at`.

### Assignments
Student assignments. Fields: `id`, `title`, `description`, `department_id`, `faculty_id`, `deadline`, `created_at`, `updated_at`.

### Notifications
In-app notifications. Fields: `id`, `user_id`, `title`, `message`, `type`, `related_id`, `is_read`, `created_at`.

---

## Testing

### Backend Tests
```bash
cd src/backend

# Run all tests
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=app
```

---

## Seeding Demo Data

To populate the database with demo users, departments, notices, and assignments, create a seed script at `src/backend/seed_full.py` and run:

```bash
cd src/backend
python seed_full.py
```

The seed script is gitignored to keep demo data out of production.

---

## Production Deployment

### Backend (e.g., Render, Railway)
1. Set environment variables (see `.env.example`)
2. Set `DEBUG=False`
3. Set `CORS_ORIGINS=https://yourdomain.com`
4. Run migrations: `alembic upgrade head`
5. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (e.g., Vercel, Netlify)
1. Set `VITE_API_URL=https://your-backend.com/api/v1`
2. Build: `npm run build`
3. Deploy: `dist/` folder

---
