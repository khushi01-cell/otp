from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timedelta
from app.database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    username=Column(String,unique=True,index=True)
    password=Column(String)

    otp = relationship("OTP", back_populates="user", uselist=False)
class OTP(Base):
    __tablename__="otp"
    id=Column(Integer,primary_key=True,index=True)
    code=Column(String)
    expires_at=Column(DateTime)
    is_used=Column(Boolean,default=False)
    user_id=Column(Integer,ForeignKey("users.id"))

    user=relationship("User",back_populates="otp")