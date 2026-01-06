from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

engine=create_engine('postgresql://postgres:Ke200207%40@localhost/pizza_delivery',
                      echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)