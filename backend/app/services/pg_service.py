from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pg import PG
from app.models.user import User

def create_pg(db: Session, pg_data, current_user: User):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create PGs")

    pg = PG(
        name=pg_data.name,
        address=pg_data.address,
        admin_id=current_user.id
    )

    db.add(pg)
    db.commit()
    db.refresh(pg)
    return pg

def get_pgs(db: Session):
    return db.query(PG).all()