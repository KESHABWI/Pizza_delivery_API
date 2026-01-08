from fastapi import FastAPI
from order_routes import order_router
from auth_routes import auth_router
from database import engine,Base
from models import User, Order

# Create tables on startup
Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(order_router)
app.include_router(auth_router)

