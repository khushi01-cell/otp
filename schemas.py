from pydantic import BaseModel,EmailStr

class SignUpSchema(BaseModel):
    username:str
    email:EmailStr
    password:str

class LoginSchema(BaseModel):
    email:EmailStr

class OTPVerifySchema(BaseModel):
    email:EmailStr
    otp:str
