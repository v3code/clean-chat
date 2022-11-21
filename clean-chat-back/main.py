from celery import Celery
from decouple import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import db


GLOBAL_ROUTE = config('GLOBAL_ROUTE', '/api/v1')


app = FastAPI()
celery = Celery("ML Service", backend=config("REDIS_URL"), broker=config("BROKER_URL"))


origins = config("ALLOWED_ORIGINS").split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

import chat.routes
import auth.routes