from fastapi import FastAPI
import models
from database import engine

from routers import otp

app=FastAPI(title="OTP service")

models.Base.metadata.create_all(bind=engine)

app.include_router(otp.router)