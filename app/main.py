from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from typing import List, Optional

from . import models, schemas, crud, auth, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Zorvyn Finance Backend", version="1.0.0")

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/records/", response_model=schemas.Record)
def create_record(
    record: schemas.RecordCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ANALYST]))
):
    return crud.create_record(db=db, record=record, user_id=current_user.id)

@app.get("/records/", response_model=List[schemas.Record])
def read_records(
    skip: int = 0, limit: int = 10,
    category: Optional[models.FinancialCategory] = None, 
    record_type: Optional[models.RecordType] = None,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None,
    global_view: bool = False,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if global_view and current_user.role == models.UserRole.VIEWER:
         raise HTTPException(status_code=403, detail="Viewers cannot access detailed company-wide records.")
         
    return crud.get_records(
        db, user=current_user, skip=skip, limit=limit, 
        category=category, record_type=record_type, search=search,
        global_view=global_view, start_date=start_date,end_date=end_date
    )

@app.get("/dashboard/my-summary")
def get_personal_summary(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_dashboard_summary(db, user_id=current_user.id, global_view=False)

@app.get("/dashboard/company-summary")
def get_company_summary(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user) 
):
    return crud.get_dashboard_summary(db, user_id=current_user.id, global_view=True)

@app.put("/records/{record_id}", response_model=schemas.Record)
def update_record(
    record_id: int, 
    record_update: schemas.RecordCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ANALYST]))
):
    updated = crud.update_record(db, record_id=record_id, user_id=current_user.id, record_update=record_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

@app.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN]))
):
    success = crud.delete_record(db, record_id=record_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return None
