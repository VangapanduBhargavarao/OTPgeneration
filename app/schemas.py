from pydantic import BaseModel

class SendOTP(BaseModel):
    phone_number:str
class VerifyOTP(BaseModel):
    otp:str

    