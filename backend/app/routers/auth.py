from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.core.database import get_db
from app.services.auth_service import signup_service, login_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    token, error = signup_service(db, user.name, user.email, user.password)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return {"access_token": token}


@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    token, error = login_service(db, user.email, user.password)

    if error:
        raise HTTPException(status_code=401, detail=error)

    # ✅ Set JWT in cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,   # 1 hour
        samesite="lax"
    )

    return {"access_token": token, "token_type": "bearer"}
