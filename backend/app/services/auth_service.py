from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def signup_service(db: Session, name: str, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None, "Email already registered"

    new_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})

    return token, None


def login_service(db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None, "Invalid email or password"

    if not verify_password(password, db_user.password_hash):
        return None, "Invalid email or password"

    token = create_access_token({"sub": str(db_user.id)})

    return token, None
