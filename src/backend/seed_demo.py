import sys
import shutil
import uuid
from pathlib import Path
from datetime import datetime, timedelta

from sqlalchemy import text

from app.core.database import SessionLocal
from app.core.security.hashing import get_password_hash
from app.models import User, Department, Profile, Notice, Assignment, Query


DEMO_PASSWORD = "demo123"
EMAIL_DOMAIN = "campusos.app"

SEED_FILES_DIR = Path(__file__).parent / "seed_files"
UPLOADS_DIR = Path(__file__).parent / "uploads" / "assignments"


def wipe_all(db):
    print("\n[1/7] Wiping existing data...")
    for table in ["notifications", "queries", "assignments", "notices", "profiles", "users", "departments"]:
        try:
            result = db.execute(text(f"DELETE FROM {table}"))
            print(f"  cleared: {table:<15} ({result.rowcount} rows)")
        except Exception as e:
            print(f"  skip {table}: {e}")
    try:
        for table in ["users", "notices", "assignments", "notifications", "profiles", "queries", "departments"]:
            db.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"))
    except Exception:
        pass
    db.commit()


DEPARTMENTS = [
    {"name": "Computer Engineering", "code": "CE"},
    {"name": "Information Technology", "code": "IT"},
    {"name": "Mechanical Engineering", "code": "ME"},
]


def seed_departments(db):
    print("\n[2/7] Creating departments...")
    dept_map = {}
    for d in DEPARTMENTS:
        dept = Department(name=d["name"], code=d["code"])
        db.add(dept)
        db.flush()
        dept_map[d["code"]] = dept
        print(f"  created: {d['name']} ({d['code']})")
    db.commit()
    return dept_map


USERS = [
    {
        "email": f"arrow@{EMAIL_DOMAIN}",
        "name": "Arrow",
        "role": "admin",
        "dept": None,
        "profile": {
            "phone": "+91 90000 00001",
            "gender": "Male",
            "designation": "System Administrator",
        },
    },
    {
        "email": f"hiren@{EMAIL_DOMAIN}",
        "name": "Hiren Barot",
        "role": "principal",
        "dept": None,
        "profile": {
            "phone": "+91 90000 00002",
            "gender": "Male",
            "qualification": "PhD",
            "specialization": "Computer Engineering",
            "experience_years": 20,
            "joining_date": "2005-06-15",
            "designation": "Principal",
        },
    },
    {
        "email": f"vyom.hod@{EMAIL_DOMAIN}",
        "name": "Vyom Dangi",
        "role": "hod",
        "dept": "CE",
        "profile": {
            "phone": "+91 90000 00003",
            "gender": "Male",
            "qualification": "M.Tech",
            "specialization": "Software Engineering",
            "experience_years": 10,
            "joining_date": "2015-07-01",
            "designation": "Head of Department",
        },
    },
    {
        "email": f"akshay.faculty@{EMAIL_DOMAIN}",
        "name": "Akshay Shah",
        "role": "faculty",
        "dept": "CE",
        "profile": {
            "phone": "+91 90000 00004",
            "gender": "Male",
            "qualification": "M.Tech",
            "specialization": "DBMS",
            "experience_years": 5,
            "joining_date": "2020-08-01",
            "designation": "Assistant Professor",
        },
    },
    {
        "email": f"rudra.faculty@{EMAIL_DOMAIN}",
        "name": "Rudra Patel",
        "role": "faculty",
        "dept": "CE",
        "profile": {
            "phone": "+91 90000 00005",
            "gender": "Male",
            "qualification": "M.E.",
            "specialization": "Networking",
            "experience_years": 4,
            "joining_date": "2021-07-15",
            "designation": "Assistant Professor",
        },
    },
    {
        "email": f"aarav.shah@{EMAIL_DOMAIN}",
        "name": "Aarav Shah",
        "role": "student",
        "dept": "CE",
        "profile": {
            "phone": "+91 90000 00006",
            "gender": "Male",
            "date_of_birth": "2004-05-12",
            "enrollment_no": "22CE001",
            "course": "Computer Engineering",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Rakesh Shah",
            "parent_phone": "+91 90000 00101",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"diya.mehta@{EMAIL_DOMAIN}",
        "name": "Diya Mehta",
        "role": "student",
        "dept": "CE",
        "profile": {
            "phone": "+91 90000 00007",
            "gender": "Female",
            "date_of_birth": "2004-08-15",
            "enrollment_no": "22CE002",
            "course": "Computer Engineering",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Sanjay Mehta",
            "parent_phone": "+91 90000 00102",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"kabir.desai@{EMAIL_DOMAIN}",
        "name": "Kabir Desai",
        "role": "student",
        "dept": "CE",
        "profile": {
            "phone": "+91 90000 00008",
            "gender": "Male",
            "date_of_birth": "2004-02-28",
            "enrollment_no": "22CE003",
            "course": "Computer Engineering",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Amit Desai",
            "parent_phone": "+91 90000 00103",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"tazin.hod@{EMAIL_DOMAIN}",
        "name": "Tazin Chauhan",
        "role": "hod",
        "dept": "IT",
        "profile": {
            "phone": "+91 90000 00009",
            "gender": "Male",
            "qualification": "M.Tech",
            "specialization": "Information Security",
            "experience_years": 12,
            "joining_date": "2013-06-01",
            "designation": "Head of Department",
        },
    },
    {
        "email": f"rahil.faculty@{EMAIL_DOMAIN}",
        "name": "Rahil Khan",
        "role": "faculty",
        "dept": "IT",
        "profile": {
            "phone": "+91 90000 00010",
            "gender": "Male",
            "qualification": "M.Tech",
            "specialization": "Cloud Computing",
            "experience_years": 5,
            "joining_date": "2020-07-01",
            "designation": "Assistant Professor",
        },
    },
    {
        "email": f"kavan.faculty@{EMAIL_DOMAIN}",
        "name": "Kavan Joshi",
        "role": "faculty",
        "dept": "IT",
        "profile": {
            "phone": "+91 90000 00011",
            "gender": "Male",
            "qualification": "M.C.A.",
            "specialization": "Web Development",
            "experience_years": 7,
            "joining_date": "2018-08-15",
            "designation": "Assistant Professor",
        },
    },
    {
        "email": f"ishaan.verma@{EMAIL_DOMAIN}",
        "name": "Ishaan Verma",
        "role": "student",
        "dept": "IT",
        "profile": {
            "phone": "+91 90000 00012",
            "gender": "Male",
            "date_of_birth": "2004-06-10",
            "enrollment_no": "22IT001",
            "course": "Information Technology",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Anil Verma",
            "parent_phone": "+91 90000 00201",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"riya.kapoor@{EMAIL_DOMAIN}",
        "name": "Riya Kapoor",
        "role": "student",
        "dept": "IT",
        "profile": {
            "phone": "+91 90000 00013",
            "gender": "Female",
            "date_of_birth": "2004-09-25",
            "enrollment_no": "22IT002",
            "course": "Information Technology",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Rohit Kapoor",
            "parent_phone": "+91 90000 00202",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"arjun.nair@{EMAIL_DOMAIN}",
        "name": "Arjun Nair",
        "role": "student",
        "dept": "IT",
        "profile": {
            "phone": "+91 90000 00014",
            "gender": "Male",
            "date_of_birth": "2004-12-05",
            "enrollment_no": "22IT003",
            "course": "Information Technology",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Suresh Nair",
            "parent_phone": "+91 90000 00203",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"rajesh.hod@{EMAIL_DOMAIN}",
        "name": "Rajesh Kumar",
        "role": "hod",
        "dept": "ME",
        "profile": {
            "phone": "+91 90000 00015",
            "gender": "Male",
            "qualification": "PhD",
            "specialization": "Thermal Engineering",
            "experience_years": 15,
            "joining_date": "2010-08-01",
            "designation": "Head of Department",
        },
    },
    {
        "email": f"yash.faculty@{EMAIL_DOMAIN}",
        "name": "Yash Trivedi",
        "role": "faculty",
        "dept": "ME",
        "profile": {
            "phone": "+91 90000 00016",
            "gender": "Male",
            "qualification": "M.Tech",
            "specialization": "Machine Design",
            "experience_years": 6,
            "joining_date": "2019-07-01",
            "designation": "Assistant Professor",
        },
    },
    {
        "email": f"dhruv.faculty@{EMAIL_DOMAIN}",
        "name": "Dhruv Solanki",
        "role": "faculty",
        "dept": "ME",
        "profile": {
            "phone": "+91 90000 00017",
            "gender": "Male",
            "qualification": "M.E.",
            "specialization": "Manufacturing",
            "experience_years": 5,
            "joining_date": "2020-08-01",
            "designation": "Assistant Professor",
        },
    },
    {
        "email": f"aditya.rao@{EMAIL_DOMAIN}",
        "name": "Aditya Rao",
        "role": "student",
        "dept": "ME",
        "profile": {
            "phone": "+91 90000 00018",
            "gender": "Male",
            "date_of_birth": "2004-01-15",
            "enrollment_no": "22ME001",
            "course": "Mechanical Engineering",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Srinivas Rao",
            "parent_phone": "+91 90000 00301",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"meera.chawla@{EMAIL_DOMAIN}",
        "name": "Meera Chawla",
        "role": "student",
        "dept": "ME",
        "profile": {
            "phone": "+91 90000 00019",
            "gender": "Female",
            "date_of_birth": "2004-03-08",
            "enrollment_no": "22ME002",
            "course": "Mechanical Engineering",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Prakash Chawla",
            "parent_phone": "+91 90000 00302",
            "address": "Ahmedabad, Gujarat",
        },
    },
    {
        "email": f"vihaan.gupta@{EMAIL_DOMAIN}",
        "name": "Vihaan Gupta",
        "role": "student",
        "dept": "ME",
        "profile": {
            "phone": "+91 90000 00020",
            "gender": "Male",
            "date_of_birth": "2004-05-22",
            "enrollment_no": "22ME003",
            "course": "Mechanical Engineering",
            "semester": 5,
            "admission_year": 2022,
            "parent_name": "Manoj Gupta",
            "parent_phone": "+91 90000 00303",
            "address": "Ahmedabad, Gujarat",
        },
    },
]


def parse_date(v):
    if isinstance(v, str):
        return datetime.strptime(v, "%Y-%m-%d").date()
    return v


def seed_users(db, dept_map):
    print("\n[3/7] Creating users and profiles...")
    hashed = get_password_hash(DEMO_PASSWORD)
    user_map = {}

    for u in USERS:
        dept_id = dept_map[u["dept"]].id if u["dept"] else None
        user = User(
            email=u["email"],
            hashed_password=hashed,
            full_name=u["name"],
            role=u["role"],
            department_id=dept_id,
            is_active=True,
            must_change_password=False,
        )
        db.add(user)
        db.flush()
        user_map[u["email"]] = user

        pd = u.get("profile") or {}
        clean = {k: (parse_date(v) if k in ("joining_date", "date_of_birth") else v) for k, v in pd.items()}
        db.add(Profile(user_id=user.id, **clean))
        print(f"  {u['role']:<10} {u['email']}")

    for email, user in user_map.items():
        if user.role == "hod" and user.department_id:
            dept = db.query(Department).filter(Department.id == user.department_id).first()
            if dept:
                dept.hod_id = user.id

    db.commit()
    return user_map


NOTICES = [
    {
        "title": "Mid-Sem Exam Schedule Released",
        "content": "Mid-semester exams begin 15th October. Timetable on department notice board.",
        "dept": None,
        "author": f"hiren@{EMAIL_DOMAIN}",
    },
    {
        "title": "Tech Fest 2026 — Register Now",
        "content": "Registrations open for Tech Fest. Last date: 25th October.",
        "dept": None,
        "author": f"hiren@{EMAIL_DOMAIN}",
    },
    {
        "title": "DBMS Practical Exam — Batch List",
        "content": "Batches posted in department office. Bring completed journals.",
        "dept": "CE",
        "author": f"akshay.faculty@{EMAIL_DOMAIN}",
    },
    {
        "title": "AWS Workshop — 14-15 Oct",
        "content": "Two-day hands-on AWS workshop. Register with Prof. Rahil by 12 Oct.",
        "dept": "IT",
        "author": f"rahil.faculty@{EMAIL_DOMAIN}",
    },
    {
        "title": "Industrial Visit — AMUL Plant",
        "content": "Visit on 19th October. Submit consent form to Prof. Yash by 15 Oct.",
        "dept": "ME",
        "author": f"yash.faculty@{EMAIL_DOMAIN}",
    },
]


def seed_notices(db, dept_map, user_map):
    print("\n[4/7] Creating notices...")
    for n in NOTICES:
        author = user_map.get(n["author"])
        if not author:
            continue
        dept_id = dept_map[n["dept"]].id if n["dept"] else None
        db.add(Notice(
            title=n["title"],
            content=n["content"],
            department_id=dept_id,
            faculty_id=author.id,
            is_published=True,
        ))
        print(f"  {n['title']}")
    db.commit()


ASSIGNMENTS = [
    {
        "title": "DBMS Assignment 3",
        "description": "Solve normalization problems from Chapter 5. Submit as PDF.",
        "dept": "CE",
        "author": f"akshay.faculty@{EMAIL_DOMAIN}",
        "due_in_days": 7,
        "seed_file": "dbms_assignment.pdf",
    },
    {
        "title": "Cloud Computing Case Study",
        "description": "Write a 2-page case study on a real-world cloud migration.",
        "dept": "IT",
        "author": f"rahil.faculty@{EMAIL_DOMAIN}",
        "due_in_days": 10,
        "seed_file": "networks_assignment.pdf",
    },
    {
        "title": "Machine Design — Gear Train",
        "description": "Design a two-stage spur gear reducer. Submit bound report.",
        "dept": "ME",
        "author": f"yash.faculty@{EMAIL_DOMAIN}",
        "due_in_days": 12,
        "seed_file": "machining_assignment.pdf",
    },
]


def seed_assignments(db, dept_map, user_map):
    print("\n[5/7] Creating assignments with files...")
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.utcnow()

    for a in ASSIGNMENTS:
        author = user_map.get(a["author"])
        if not author:
            continue
        dept_id = dept_map[a["dept"]].id

        src = SEED_FILES_DIR / a["seed_file"]
        file_path = None
        file_size = None
        file_name = None
        file_type = None

        if src.exists():
            ext = src.suffix.lower()
            dest_name = f"{uuid.uuid4().hex}{ext}"
            dest = UPLOADS_DIR / dest_name
            shutil.copyfile(src, dest)
            file_path = str(dest)
            file_size = dest.stat().st_size
            file_name = a["seed_file"]
            file_type = "application/pdf" if ext == ".pdf" else "application/octet-stream"
            print(f"  {a['title']}  (file: {a['seed_file']})")
        else:
            print(f"  {a['title']}  missing seed file: {a['seed_file']}")

        db.add(Assignment(
            title=a["title"],
            description=a["description"],
            department_id=dept_id,
            faculty_id=author.id,
            deadline=now + timedelta(days=a["due_in_days"]),
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
        ))

    db.commit()


QUERIES = [
    {
        "title": "How to submit DBMS assignment?",
        "description": "I missed the submission link. Where do I upload the PDF?",
        "student": f"aarav.shah@{EMAIL_DOMAIN}",
        "reply": "Upload it on the Assignments tab. Click Download on the assignment card.",
        "replied_by": f"akshay.faculty@{EMAIL_DOMAIN}",
    },
    {
        "title": "AWS Workshop eligibility?",
        "description": "Can second-year students attend the AWS workshop?",
        "student": f"ishaan.verma@{EMAIL_DOMAIN}",
        "reply": None,
        "replied_by": None,
    },
    {
        "title": "Library timings during exams",
        "description": "What are the extended hours during the mid-semester exams?",
        "student": f"aditya.rao@{EMAIL_DOMAIN}",
        "reply": None,
        "replied_by": None,
    },
]


def seed_queries(db, user_map):
    print("\n[6/7] Creating queries...")
    for q in QUERIES:
        student = user_map.get(q["student"])
        if not student or not student.department_id:
            continue

        reply_text = q.get("reply")
        replier = user_map.get(q.get("replied_by")) if q.get("replied_by") else None

        row = Query(
            title=q["title"],
            description=q["description"],
            student_id=student.id,
            department_id=student.department_id,
            status="answered" if reply_text else "open",
        )
        if reply_text and replier:
            row.reply = reply_text
            row.replied_by_id = replier.id
            row.replied_at = datetime.utcnow()

        db.add(row)
        print(f"  {q['title']}  ({'answered' if reply_text else 'open'})")

    db.commit()


def main():
    db = SessionLocal()
    try:
        wipe_all(db)
        dept_map = seed_departments(db)
        user_map = seed_users(db, dept_map)
        seed_notices(db, dept_map, user_map)
        seed_assignments(db, dept_map, user_map)
        seed_queries(db, user_map)

        print("\n" + "=" * 60)
        print("  DEMO DATA READY")
        print("=" * 60)
        print(f"  Password for all accounts: {DEMO_PASSWORD}")
        print("=" * 60)
        print("\n  Try logging in as:\n")
        print(f"    Admin      : arrow@{EMAIL_DOMAIN}")
        print(f"    Principal  : hiren@{EMAIL_DOMAIN}")
        print(f"    HOD (CE)   : vyom.hod@{EMAIL_DOMAIN}")
        print(f"    Faculty CE : akshay.faculty@{EMAIL_DOMAIN}")
        print(f"    Student CE : aarav.shah@{EMAIL_DOMAIN}")
        print(f"    Student IT : ishaan.verma@{EMAIL_DOMAIN}")
        print(f"    Student ME : aditya.rao@{EMAIL_DOMAIN}")
        print("\n" + "=" * 60 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\nSeed failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()