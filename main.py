from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.exc import OperationalError
import time
from database import engine, Base
from order_routes import order_router
from auth_routes import auth_router
from models import User, Order


@asynccontextmanager
async def lifespan(app: FastAPI):
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected & tables created")
            break
        except OperationalError:
            retries -= 1
            print("⏳ Waiting for database...")
            time.sleep(2)

    yield  # 🔹 App runs here

    # 🔻 Optional shutdown logic
    print("🛑 Application shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(order_router)
app.include_router(auth_router)