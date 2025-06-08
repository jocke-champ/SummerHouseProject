from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.database import Base, engine

# Swedish timezone
swedish_tz = pytz.timezone('Europe/Stockholm')

def swedish_now():
    return datetime.now(swedish_tz)

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    author = Column(String)
    priority = Column(String, default="medium")
    created_at = Column(DateTime, default=swedish_now)
    
    images = relationship("TodoImage", back_populates="todo", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="todo", cascade="all, delete-orphan")

class TodoImage(Base):
    __tablename__ = "todo_images"
    
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todos.id"))
    filename = Column(String)
    original_name = Column(String)
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=swedish_now)
    
    todo = relationship("Todo", back_populates="images")

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    created_by = Column(String)
    created_at = Column(DateTime, default=swedish_now)
    is_completed = Column(Boolean, default=False)
    
    items = relationship("ShoppingItem", back_populates="shopping_list", cascade="all, delete-orphan")

class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"))
    item_name = Column(String)
    quantity = Column(Float, default=1.0)
    unit = Column(String, default="pcs")  # pcs, kg, lbs, bottles, etc.
    notes = Column(Text)
    is_checked = Column(Boolean, default=False)
    checked_by = Column(String)
    checked_at = Column(DateTime)
    added_by = Column(String)
    added_at = Column(DateTime, default=swedish_now)
    
    shopping_list = relationship("ShoppingList", back_populates="items")
    
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todos.id"))
    author = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    todo = relationship("Todo", back_populates="comments")

# Create tables
Base.metadata.create_all(bind=engine)