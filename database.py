from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL="postgresql://postgres:icqRyttJAmbbQxigspPMMhlFHNKEXFPK@postgres.railway.internal:5432/railway" #FOR RAILWAY DEPLOYMENT
#DATABASE_URL="postgresql://postgres:Ke200207%40@localhost/pizza_delivery". FOR LOCAL USE NO DOCKER
#DATABASE_URL=os.getenv("DATABASE_URL") 

engine=create_engine(DATABASE_URL, echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)