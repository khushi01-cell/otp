from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas, utils
from app.database import SessionLocal, engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup")
def signup(user_data: schemas.SignUpSchema, db: Session = Depends(get_db)):
    try:
        if db.query(models.User).filter(models.User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        user = models.User(**user_data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error during signup")
    finally:
        db.close()


@app.post("/login")
def login(login_data: schemas.LoginSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == login_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = utils.create_otp(db, user)
        return {"message": "OTP sent to email (simulated)", "otp": otp.code}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error during login")
    finally:
        db.close()


@app.post("/verify")
def verify(otp_data: schemas.OTPVerifySchema, db: Session = Depends(get_db)):
    try:
        success, message = utils.verify_otp(db, otp_data.email, otp_data.otp)
        if not success:
            raise HTTPException(status_code=400, detail=message)
        return {"message": "OTP verified successfully"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error during OTP verification")
    finally:
        db.close()



