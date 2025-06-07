from fastapi import APIRouter, HTTPException, Form, Depends, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models import Todo
from app.dependencies import get_db
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request, 
    sort_by: str = Query("date", regex="^(date|priority|author|title)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    filter_priority: Optional[str] = Query(None),  # Ta bort regex här
    filter_author: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Konvertera tomma strängar till None
    if filter_priority == "":
        filter_priority = None
    if filter_author == "":
        filter_author = None
    
    # Validera filter_priority manuellt om det inte är None
    if filter_priority is not None and filter_priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Invalid priority filter")
    # Start with base query
    query = db.query(Todo)
    
    # Apply filters
    if filter_priority:
        query = query.filter(Todo.priority == filter_priority)
    
    if filter_author:
        query = query.filter(Todo.author.ilike(f"%{filter_author}%"))
    
    # Apply sorting
    if sort_by == "date":
        if order == "desc":
            query = query.order_by(desc(Todo.created_at))
        else:
            query = query.order_by(asc(Todo.created_at))
    elif sort_by == "priority":
        # Custom priority order: high -> medium -> low
        priority_order = {"high": 1, "medium": 2, "low": 3}
        if order == "desc":
            # High priority first
            query = query.order_by(
                desc(Todo.priority == "high"),
                desc(Todo.priority == "medium"),
                desc(Todo.priority == "low")
            )
        else:
            # Low priority first
            query = query.order_by(
                asc(Todo.priority == "low"),
                asc(Todo.priority == "medium"),
                asc(Todo.priority == "high")
            )
    elif sort_by == "author":
        if order == "desc":
            query = query.order_by(desc(Todo.author))
        else:
            query = query.order_by(asc(Todo.author))
    elif sort_by == "title":
        if order == "desc":
            query = query.order_by(desc(Todo.title))
        else:
            query = query.order_by(asc(Todo.title))
    
    todos = query.all()
    
    # Get unique authors for filter dropdown
    authors = db.query(Todo.author).distinct().all()
    authors = [author[0] for author in authors]
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "todos": todos,
        "authors": authors,
        "current_sort": sort_by,
        "current_order": order,
        "current_priority_filter": filter_priority,
        "current_author_filter": filter_author,
    })

@router.get("/api/todos")
async def get_todos(
    sort_by: str = Query("date", regex="^(date|priority|author|title)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    filter_priority: Optional[str] = Query(None),  # Ta bort regex här
    filter_author: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Konvertera tomma strängar till None
    if filter_priority == "":
        filter_priority = None
    if filter_author == "":
        filter_author = None
    
    # Validera filter_priority manuellt
    if filter_priority is not None and filter_priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Invalid priority filter")
    
    query = db.query(Todo)
    
    if filter_priority:
        query = query.filter(Todo.priority == filter_priority)
    
    if filter_author:
        query = query.filter(Todo.author.ilike(f"%{filter_author}%"))
    
    if sort_by == "date":
        if order == "desc":
            query = query.order_by(desc(Todo.created_at))
        else:
            query = query.order_by(asc(Todo.created_at))
    elif sort_by == "priority":
        if order == "desc":
            query = query.order_by(
                desc(Todo.priority == "high"),
                desc(Todo.priority == "medium"),
                desc(Todo.priority == "low")
            )
        else:
            query = query.order_by(
                asc(Todo.priority == "low"),
                asc(Todo.priority == "medium"),
                asc(Todo.priority == "high")
            )
    elif sort_by == "author":
        if order == "desc":
            query = query.order_by(desc(Todo.author))
        else:
            query = query.order_by(asc(Todo.author))
    elif sort_by == "title":
        if order == "desc":
            query = query.order_by(desc(Todo.title))
        else:
            query = query.order_by(asc(Todo.title))
    
    return query.all()

@router.post("/api/todos")
async def create_todo(
    title: str = Form(...),
    description: str = Form(...),
    author: str = Form(...),
    priority: str = Form("medium"),
    db: Session = Depends(get_db)
):
    todo = Todo(
        title=title,
        description=description,
        author=author,
        priority=priority
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return RedirectResponse(url="/", status_code=303)

@router.get("/todo/{todo_id}")
async def get_todo_detail(todo_id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("todo_detail.html", {
        "request": request,
        "todo": todo
    })