from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth_schemas import UserLogin, UserRegister, Token, ChangePassword
from app.services.auth_service import AuthService
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