import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For Vercel deployment, use in-memory database or environment variable
# In production, you might want to use a persistent database like PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./summer_house.db")

if "vercel" in os.getenv("VERCEL_URL", "") or os.getenv("VERCEL"):
    # Use in-memory SQLite for Vercel (data won't persist)
    DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()