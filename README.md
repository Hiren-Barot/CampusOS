# CampusOS

A centralized student & department management platform for colleges. Consolidates notices, assignments, departments, and user management into a single role-based system.

Built with **FastAPI** (backend) + **React + Vite** (frontend) + **PostgreSQL** (database).

---

## Features

### Role-Based Access (5 Roles)
- **Admin** — System management, user CRUD, department CRUD
- **Principal** — College-wide oversight, HOD management
- **HOD** — Department management, faculty/student management
- **Faculty** — Notice and assignment creation, student management
- **Student** — Read-only access to notices and assignments, assignment download

### Core Features
- JWT authentication with bcrypt password hashing
- Auto-generated temporary passwords for new users
- Email delivery of welcome credentials via SMTP (non-blocking, runs in background)
- Department-scoped visibility (users see their own department)
- Author-only edit/delete for notices and assignments
- "All Departments" notices for Admin/Principal
- In-app notification system with unread count
- Full-text search across notices and assignments
- Role-based dashboards
- Assignment file uploads — PDF, PPT, DOCX, JPG, PNG (max 10 MB)
- Assignment file downloads — authenticated, blob-fetched
- Extended profile fields per role (student / faculty / admin)
- Users edit their own profile from the Profile page
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
| aiosmtplib | Async SMTP email |
| python-multipart | File upload parsing |

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
CampusOS/
├── src/
│   ├── backend/
│   │   ├── alembic/                  # DB migrations
│   │   │   ├── versions/
│   │   │   └── env.py
│   │   ├── app/
│   │   │   ├── api/v1/               # API routes
│   │   │   ├── core/                 # Config, DB, security
│   │   │   ├── models/               # SQLAlchemy models
│   │   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── services/             # Business logic
│   │   │   ├── repositories/         # Data access
│   │   │   ├── utils/                # Helpers
│   │   │   ├── main.py               # App entry
│   │   │   └── middleware.py         # Logging middleware
│   │   ├── uploads/                  # Assignment files (gitignored)
│   │   ├── alembic.ini
│   │   ├── requirements.txt
│   │   └── .env.example
│   └── frontend/
│       ├── src/
│       │   ├── components/           # Reusable UI
│       │   ├── pages/                # Route pages
│       │   ├── services/             # API clients
│       │   ├── context/              # Auth context
│       │   ├── hooks/                # Custom hooks
│       │   ├── utils/                # Helpers
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── package.json
│       ├── tailwind.config.js
│       ├── vite.config.js
│       └── .env.example
├── .gitignore
└── README.md
```

---

## Setup Instructions

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** and **npm**
- **PostgreSQL 15+**
- **Git**

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd CampusOS
```

### 2. Backend Setup

```bash
cd src/backend

# Create and activate virtual environment
python -m venv .venv

# Windows (Git Bash / PowerShell):
source .venv/Scripts/activate

# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Create the database in PostgreSQL:**

```bash
psql -U postgres

CREATE DATABASE campusos;
CREATE USER campusos_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE campusos TO campusos_user;

\c campusos
GRANT ALL ON SCHEMA public TO campusos_user;
ALTER SCHEMA public OWNER TO campusos_user;
\q
```

**Configure environment:**

```bash
cp .env.example .env
# Edit .env with your actual values:
#   - DATABASE_URL (with your PostgreSQL credentials)
#   - JWT_SECRET_KEY (any random string)
#   - SMTP_USER / SMTP_PASSWORD (Gmail App Password, optional — see below)
```

**Run migrations (creates all tables):**

```bash
alembic upgrade head
```

**Create the uploads folder:**

```bash
mkdir -p uploads/assignments
touch uploads/assignments/.gitkeep
```

**Start the backend server:**

```bash
uvicorn app.main:app --reload
```

- Backend: **http://localhost:8000**
- Swagger docs: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
# In a new terminal, from project root
cd src/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Default: VITE_API_URL=http://localhost:8000/api/v1

# Start dev server
npm run dev
```

- Frontend: **http://localhost:5173**

### 4. Gmail SMTP Setup (for welcome emails)

Optional but recommended for a full demo.

1. Create a Gmail account (e.g. `campusos.noreply@gmail.com`)
2. Enable **2-Step Verification** on that account
3. Generate an **App Password**: https://myaccount.google.com/apppasswords
4. Put the 16-character password in backend `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=campusos.noreply@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   EMAIL_FROM_ADDRESS=campusos.noreply@gmail.com
   EMAIL_FROM_NAME=CampusOS
   ```

If SMTP credentials are not configured, emails are silently skipped — the app still works.

---

## Demo Accounts

Run the seed script OR create users manually through the Admin dashboard.

Default password for demo accounts: `demo123`

| Role | Email |
|------|-------|
| Admin | admin@campusos.app |
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
| POST | `/api/v1/auth/login` | Login (returns JWT) |
| GET | `/api/v1/auth/me` | Current user profile |
| POST | `/api/v1/auth/change-password` | Change own password |

### Users
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/users/` | Admin, Principal, HOD, Faculty |
| POST | `/api/v1/users/` | Admin, Principal, HOD, Faculty (role-scoped) |
| GET | `/api/v1/users/me` | All authenticated |
| GET | `/api/v1/users/{id}` | Role-based |
| PUT | `/api/v1/users/{id}` | Self OR higher authority |
| DELETE | `/api/v1/users/{id}` | Higher authority only |
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
| POST | `/api/v1/assignments/` | Faculty only (multipart/form-data) |
| GET | `/api/v1/assignments/{id}/download` | Role-scoped |
| PUT | `/api/v1/assignments/{id}` | Author only |
| DELETE | `/api/v1/assignments/{id}` | Author only |

### Notifications
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/v1/notifications/` | Own notifications |
| GET | `/api/v1/notifications/unread/count` | Unread count |
| PATCH | `/api/v1/notifications/{id}/read` | Mark as read |

Full API documentation at `/docs` (Swagger UI) when running in debug mode.

---

## Database Schema

### Users
All user accounts. Fields: `id`, `email`, `hashed_password`, `full_name`, `role`, `department_id`, `is_active`, `must_change_password`, `created_at`, `updated_at`.

### Profiles
Role-specific user details. One-to-one with User. Fields: `id`, `user_id`, `phone`, `gender`, `date_of_birth`, `address`, `enrollment_no`, `course`, `semester`, `admission_year`, `parent_name`, `parent_phone`, `qualification`, `specialization`, `experience_years`, `joining_date`, `designation`, `created_at`, `updated_at`.

### Departments
Academic departments. Fields: `id`, `name`, `code`, `hod_id`, `created_at`.

### Notices
Department announcements. Fields: `id`, `title`, `content`, `department_id` (nullable for "all departments"), `faculty_id`, `is_published`, `created_at`, `updated_at`.

### Assignments
Student assignments with optional file. Fields: `id`, `title`, `description`, `department_id`, `faculty_id`, `deadline`, `file_path`, `file_name`, `file_size`, `file_type`, `created_at`, `updated_at`.

### Notifications
In-app notifications. Fields: `id`, `user_id`, `title`, `message`, `type`, `related_id`, `is_read`, `created_at`.

---

## Development Workflow

When you pull new changes from a teammate:

```bash
git pull

# Backend: apply any new migrations
cd src/backend
source .venv/Scripts/activate       # or .venv/bin/activate
alembic upgrade head

# Restart backend
uvicorn app.main:app --reload
```

When you add/change a model:

```bash
cd src/backend
source .venv/Scripts/activate
alembic revision --autogenerate -m "short description"
# ALWAYS open the generated file and check what it does!
alembic upgrade head
```

**Never edit migration files by hand unless autogenerate fails.**

---

## File Uploads

Assignment files are stored on local disk at `src/backend/uploads/assignments/`.

- Max size: **10 MB**
- Allowed types: **PDF, PPT, PPTX, DOC, DOCX, JPG, JPEG, PNG**
- Filenames are stored as random UUIDs on disk to prevent collisions and path traversal
- Original filename preserved in the DB (`file_name` column) and shown to users
- `uploads/` folder is gitignored — only the folder structure (`.gitkeep`) is committed

For production, replace local disk storage with S3 / Cloudinary / similar.

---