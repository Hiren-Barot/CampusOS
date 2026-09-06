from fastapi import APIRouter

from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .department_routes import router as department_router
from .notice_routes import router as notice_router
from .assignment_routes import router as assignment_router
from .notifications_routes import router as notification_router
from .search_routes import router as search_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(department_router)
router.include_router(notice_router)
router.include_router(assignment_router)
router.include_router(notification_router)
router.include_router(search_router)

__all__ = ["router"]

