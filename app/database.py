import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For Vercel deployment, use in-memory database or environment variable
# In production, you might want to use a persistent database like PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./summer_house.db")

# Check if running on Vercel
is_vercel = os.getenv("VERCEL") == "1" or "vercel" in os.getenv("VERCEL_URL", "").lower()

if is_vercel:
    # Use in-memory SQLite for Vercel (data won't persist)
    DATABASE_URL = "sqlite:///:memory:"
    print("Using in-memory SQLite for Vercel deployment")

try:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
        echo=False  # Set to True for debugging
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    print(f"Database configured with URL: {DATABASE_URL}")
    
except Exception as e:
    print(f"Error configuring database: {e}")
    # Fallback configuration
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()