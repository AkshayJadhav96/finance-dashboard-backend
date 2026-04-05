from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

class RecordType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class FinancialCategory(str, enum.Enum):
    SALARY = "salary"
    FOOD = "food"
    RENT = "rent"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    TRANSPORT = "transport"
    OTHER = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER,nullable=False)
    is_active = Column(Boolean, default=True,nullable=False)

    records = relationship("Record", back_populates="owner",cascade="all, delete-orphan")

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(RecordType),nullable=False)
    category = Column(Enum(FinancialCategory),default=FinancialCategory.OTHER, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String)

    is_deleted = Column(Boolean, default=False, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"),index=True,nullable=False)
    owner = relationship("User", back_populates="records")
