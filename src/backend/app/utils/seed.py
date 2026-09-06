import logging
from sqlalchemy.orm import Session
from app.core.security.hashing import get_password_hash
from app.models.user_model import User
from app.models.department_model import Department
from .password_generator import generate_temp_password

logger = logging.getLogger(__name__)


def seed_initial_data(db: Session):
    departments_data = [
        {"name": "Computer Engineering", "code": "CE"},
        {"name": "Information Technology", "code": "IT"},
        {"name": "Mechanical Engineering", "code": "ME"},
        {"name": "Civil Engineering", "code": "CV"},
        {"name": "Electrical Engineering", "code": "EE"},
    ]
    
    created_departments = {}
    for dept_data in departments_data:
        existing_dept = db.query(Department).filter(
            Department.code == dept_data["code"]
        ).first()
        
        if not existing_dept:
            department = Department(**dept_data)
            db.add(department)
            db.flush()
            created_departments[dept_data["code"]] = department
            logger.info(f"Created department: {dept_data['name']} ({dept_data['code']})")
        else:
            created_departments[dept_data["code"]] = existing_dept
            logger.info(f"Department already exists: {dept_data['name']} ({dept_data['code']})")
    
    db.commit()
    
    users_data = [
        {
            "email": "admin@campusos.edu",
            "full_name": "System Admin",
            "role": "admin",
            "department_id": None,
            "is_active": True,
            "must_change_password": True,
        },
        {
            "email": "principal@campusos.edu",
            "full_name": "College Principal",
            "role": "principal",
            "department_id": None,
            "is_active": True,
            "must_change_password": True,
        },
        {
            "email": "hod.ce@campusos.edu",
            "full_name": "HOD Computer Engineering",
            "role": "hod",
            "department_id": created_departments["CE"].id,
            "is_active": True,
            "must_change_password": True,
        },
        {
            "email": "faculty.ce@campusos.edu",
            "full_name": "Faculty Computer Engineering",
            "role": "faculty",
            "department_id": created_departments["CE"].id,
            "is_active": True,
            "must_change_password": True,
        },
        {
            "email": "student.ce@campusos.edu",
            "full_name": "Student Computer Engineering",
            "role": "student",
            "department_id": created_departments["CE"].id,
            "is_active": True,
            "must_change_password": True,
        },
    ]
    
    created_users = {}
    for user_data in users_data:
        existing_user = db.query(User).filter(
            User.email == user_data["email"]
        ).first()
        
        if not existing_user:
            temp_password = generate_temp_password()
            hashed_password = get_password_hash(temp_password)
            
            user = User(
                email=user_data["email"],
                hashed_password=hashed_password,
                full_name=user_data["full_name"],
                role=user_data["role"],
                department_id=user_data["department_id"],
                is_active=user_data["is_active"],
                must_change_password=user_data["must_change_password"],
            )
            db.add(user)
            db.flush()
            created_users[user_data["email"]] = {
                "user": user,
                "temp_password": temp_password,
            }
            logger.info(
                f"Created user: {user_data['full_name']} ({user_data['role']}) "
                f"→ Temp password: {temp_password}"
            )
        else:
            created_users[user_data["email"]] = {
                "user": existing_user,
                "temp_password": None,
            }
            logger.info(f"User already exists: {user_data['full_name']} ({user_data['role']})")
    
    hod_user = db.query(User).filter(User.email == "hod.ce@campusos.edu").first()
    if hod_user:
        ce_dept = created_departments.get("CE")
        if ce_dept and not ce_dept.hod_id:
            ce_dept.hod_id = hod_user.id
            db.commit()
            logger.info(f"Assigned HOD to CE department: {hod_user.full_name}")
    
    db.commit()
    
    return {
        "departments": created_departments,
        "users": created_users,
    }


def run_seed(db: Session):
    try:
        result = seed_initial_data(db)
        logger.info("✅ Seed data created successfully!")
        return result
    except Exception as e:
        logger.error(f"❌ Failed to seed data: {str(e)}")
        db.rollback()
        raise