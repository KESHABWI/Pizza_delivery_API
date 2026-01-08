from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Ke200207%40@localhost/pizza_delivery")

engine=create_engine(DATABASE_URL, echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)