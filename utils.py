import random
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.models import OTP,User
from sqlalchemy.exc import SQLAlchemyError

def generate_otp():
    return str(random.randint(100000,999999))
def create_otp(db:Session,user:User):
    code=generate_otp()
    otp=OTP(
        code=code,
        expires_at=datetime.utcnow()+timedelta(seconds=30),
        user=user,
        is_used=False,
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    print(f"Your OTP is : {code}")
    return otp



def verify_otp(db: Session, email: str, otp_input: str):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.otp:
            return False, "User or OTP not found"

        otp = user.otp
        if otp.is_used:
            return False, "OTP already used"

        if datetime.utcnow() > otp.expires_at:
            # OTP expired, delete and resend a new one
            db.delete(otp)
            db.commit()
            new_otp = create_otp(db, user)
            return False, f"OTP expired. New OTP sent: {new_otp.code}"

        if otp.code != otp_input:
            return False, "Incorrect OTP"

        otp.is_used = True
        db.commit()
        return True, "OTP verified"

    except SQLAlchemyError:
        db.rollback()
        return False, "Database error during OTP verification"
