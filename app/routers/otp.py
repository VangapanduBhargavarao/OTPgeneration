from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
import random,hashlib
import models,schemas
from database import get_db
from twilio.rest import Client


from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER
)

router=APIRouter(
    prefix='/otp',
    tags=["OTP"]
)

client=Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)


def generate_otp()->str:
    return str(random.randint(1000,9999))

def hash_otp(otp:str)->str:
    return hashlib.sha256(otp.encode()).hexdigest()

def otp_expiry_time():
    return datetime.utcnow()+timedelta(minutes=2)

def send_otp_sms(phone_number:str,otp:str):
    message=f"your OTP is {otp}"
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=message
    )

# send otp
@router.post("/send",status_code=status.HTTP_201_CREATED)
def send_otp(data:schemas.SendOTP,db:Session=Depends(get_db)):
    otp=generate_otp()
    otp_hash=hash_otp(otp)

    record=models.OTP(
        phone_number=data.phone_number,
        otp_hash=otp_hash,
        expires_at=otp_expiry_time()
    )
    db.add(record)
    db.commit()
    send_otp_sms(data.phone_number,otp)
    ## twilo otp sending

    return {"detail":"OTP sent sucessfully"}

@router.post("/verify")
def verify_otp(data: schemas.VerifyOTP,db: Session=Depends(get_db)):
    otp_hash=hash_otp(data.otp)
    record=db.query(models.OTP).filter(
        models.OTP.otp_hash==otp_hash,
        models.OTP.is_used==False,
        models.OTP.expires_at>datetime.utcnow()
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    record.is_used=True
    db.commit()
    return {
        "detail":"OTP verified"
    }
    