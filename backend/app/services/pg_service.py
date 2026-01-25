from sqlalchemy.orm import Session
from app.models.pg import PG

def create_pg(db: Session, name: str, location: str):
    pg = PG(name=name, location=location)
    db.add(pg)
    db.commit()
    db.refresh(pg)
    return pg

def get_pgs(db: Session):
    return db.query(PG).all()
