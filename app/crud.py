from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):

    hashed_pwd = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_record(db: Session, record: schemas.RecordCreate, user_id: int):
    db_record = models.Record(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: Session, user: models.User, skip: int = 0, limit: int = 10, 
                category: str = None, record_type: str = None, search: str = None, global_view: bool = False):
    
    query = db.query(models.Record).filter(models.Record.is_deleted == False)
    
    if not global_view:
        query = query.filter(models.Record.user_id == user.id)
    
    elif user.role == models.UserRole.VIEWER:
        return []

    if search:
        query = query.filter(models.Record.description.ilike(f"%{search}%"))
    if category:
        query = query.filter(models.Record.category == category)
    if record_type:
        query = query.filter(models.Record.type == record_type)
        
    return query.offset(skip).limit(limit).all()

def get_dashboard_summary(db: Session, user_id: int, global_view: bool = False):

    base_filter = [models.Record.is_deleted == False]
    if not global_view:
        base_filter.append(models.Record.user_id == user_id)

    total_income = db.query(func.sum(models.Record.amount)).filter(
        *base_filter, models.Record.type == models.RecordType.INCOME
    ).scalar() or 0.0

    total_expense = db.query(func.sum(models.Record.amount)).filter(
        *base_filter, models.Record.type == models.RecordType.EXPENSE
    ).scalar() or 0.0

    category_totals = db.query(
        models.Record.category, 
        func.sum(models.Record.amount)
    ).filter(*base_filter).group_by(models.Record.category).all()

    return {
        "scope": "Company-Wide" if global_view else "Personal",
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "category_breakdown": {cat.value if hasattr(cat, 'value') else cat: amt for cat, amt in category_totals}
    }

def update_record(db: Session, record_id: int, user_id: int, record_update: schemas.RecordCreate):
    db_record = db.query(models.Record).filter(models.Record.id == record_id, models.Record.user_id == user_id, models.Record.is_deleted == False).first()
    if not db_record:
        return None
    
    for key, value in record_update.model_dump().items():
        setattr(db_record, key, value)
        
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int, user_id: int):
    db_record = db.query(models.Record).filter(
        models.Record.id == record_id, 
        models.Record.user_id == user_id,
        models.Record.is_deleted == False
    ).first()

    if not db_record:
        return False
    
    db_record.is_deleted = True
    db.commit()
    return True
