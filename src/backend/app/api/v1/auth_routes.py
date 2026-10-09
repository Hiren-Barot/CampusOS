from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth_schemas import (
    UserLogin,
    UserRegister,
    Token,
    ChangePassword,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.auth_service import AuthService
from app.services.email_service import email_service
from app.services.user_service import UserService
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    user = auth_service.register_user(user_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    access_token = auth_service.create_access_token(user)

    return Token(
        access_token=access_token,
        token_type="bearer",
        must_change_password=user.must_change_password,
    )


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(user)

    return Token(
        access_token=access_token,
        token_type="bearer",
        must_change_password=user.must_change_password,
    )


@router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    auth_service = AuthService(db)

    user = auth_service.authenticate_user(
        UserLogin(email=current_user.email, password=password_data.current_password)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    success = user_service.change_password(
        user_id=current_user.id,
        new_password=password_data.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password",
        )

    return {"message": "Password changed successfully"}


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service._enrich_user(current_user)


@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    result = auth_service.create_password_reset_token(payload.email)

    if result:
        user, token = result
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        try:
            await email_service.send_password_reset_email(
                to_email=user.email,
                full_name=user.full_name,
                reset_url=reset_url,
            )
        except Exception:
            pass

    return {
        "message": "If an account exists for that email, a reset link has been sent."
    }


@router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    success = auth_service.reset_password_with_token(
        token=payload.token,
        new_password=payload.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    return {"message": "Password reset successfully. You can now log in."}