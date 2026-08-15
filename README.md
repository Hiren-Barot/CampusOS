# CampusOS

A Centralized Student & Department Management Platform

## Overview
CampusOS is a centralized platform for student-department communication in educational institutions. It replaces fragmented communication channels with a unified, role-based system.

## Tech Stack
- **Backend:** FastAPI, Python 3.11+, PostgreSQL, SQLAlchemy
- **Frontend:** React.js, Tailwind CSS

## Roles
1. **Admin** - System Manager
2. **Principal** - Academic Head
3. **HOD** - Department Head
4. **Faculty** - Teachers
5. **Student** - Read-only access

## Setup Instructions

### Backend Setup
```bash
# Clone the repository
git clone <repo-url>
cd campusos/src/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials

# Run migrations
alembic upgrade head

# Run server
uvicorn app.main:app --reload