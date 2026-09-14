import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security.hashing import get_password_hash
from app.models.user_model import User
from app.models.department_model import Department
from app.models.notice_model import Notice
from app.models.assignment_model import Assignment

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_admin(db_session):
    """Create a test admin user."""
    admin = User(
        email="admin@test.com",
        hashed_password=get_password_hash("Admin@123"),
        full_name="Test Admin",
        role="admin",
        is_active=True,
        must_change_password=False,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def test_principal(db_session):
    principal = User(
        email="principal@test.com",
        hashed_password=get_password_hash("Principal@123"),
        full_name="Test Principal",
        role="principal",
        is_active=True,
        must_change_password=False,
    )
    db_session.add(principal)
    db_session.commit()
    db_session.refresh(principal)
    return principal


@pytest.fixture
def test_department(db_session):
    dept = Department(
        name="Computer Engineering",
        code="CE",
    )
    db_session.add(dept)
    db_session.commit()
    db_session.refresh(dept)
    return dept

@pytest.fixture
def test_hod(db_session, test_department):
    hod = User(
        email="hod@test.com",
        hashed_password=get_password_hash("HOD@123"),
        full_name="Test HOD",
        role="hod",
        department_id=test_department.id,
        is_active=True,
        must_change_password=False,
    )
    db_session.add(hod)
    db_session.commit()
    db_session.refresh(hod)
    
    from app.repositories.department_repository import DepartmentRepository
    dept_repo = DepartmentRepository(db_session)
    dept_repo.update(test_department.id, hod_id=hod.id)
    
    return hod


@pytest.fixture
def test_faculty(db_session, test_department):
    faculty = User(
        email="faculty@test.com",
        hashed_password=get_password_hash("Faculty@123"),
        full_name="Test Faculty",
        role="faculty",
        department_id=test_department.id,
        is_active=True,
        must_change_password=False,
    )
    db_session.add(faculty)
    db_session.commit()
    db_session.refresh(faculty)
    return faculty


@pytest.fixture
def test_student(db_session, test_department):
    student = User(
        email="student@test.com",
        hashed_password=get_password_hash("Student@123"),
        full_name="Test Student",
        role="student",
        department_id=test_department.id,
        is_active=True,
        must_change_password=False,
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student


@pytest.fixture
def test_notice(db_session, test_department, test_faculty):
    notice = Notice(
        title="Test Notice",
        content="This is a test notice content.",
        department_id=test_department.id,
        faculty_id=test_faculty.id,
        is_published=True,
    )
    db_session.add(notice)
    db_session.commit()
    db_session.refresh(notice)
    return notice


@pytest.fixture
def test_assignment(db_session, test_department, test_faculty):
    from datetime import datetime, timedelta
    
    assignment = Assignment(
        title="Test Assignment",
        description="This is a test assignment.",
        department_id=test_department.id,
        faculty_id=test_faculty.id,
        deadline=datetime.now() + timedelta(days=7),
    )
    db_session.add(assignment)
    db_session.commit()
    db_session.refresh(assignment)
    return assignment


@pytest.fixture
def auth_headers_admin(test_admin):
    return {"user": test_admin}


@pytest.fixture
def auth_headers_principal(test_principal):
    return {"user": test_principal}


@pytest.fixture
def auth_headers_hod(test_hod):
    return {"user": test_hod}


@pytest.fixture
def auth_headers_faculty(test_faculty):
    return {"user": test_faculty}


@pytest.fixture
def auth_headers_student(test_student):
    return {"user": test_student}