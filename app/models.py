from sqlalchemy import Column,Integer,String,DateTime,Boolean

from datetime import datetime

from database import Base

class OTP(Base):
    __tablename__="otp"
    
    id=Column(Integer,primary_key=True,index=True)
    phone_number=Column(String,index=True)
    otp_hash=Column(String,index=True)
    expires_at=Column(DateTime,index=True)
    is_used=Column(Boolean,default=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    
