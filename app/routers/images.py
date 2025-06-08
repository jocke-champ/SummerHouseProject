from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import Todo, TodoImage
from app.dependencies import get_db
import os
import uuid
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Ensure uploads directory exists
os.makedirs("static/uploads", exist_ok=True)

def is_htmx_request(request: Request) -> bool:
    """Check if the request is coming from htmx"""
    return request.headers.get("HX-Request") == "true"

@router.post("/api/todos/{todo_id}/images")
async def upload_image(
    todo_id: int,
    request: Request,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    # Check if todo exists
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    uploaded_files = []
    
    for file in files:
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"static/uploads/{unique_filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Save to database
        todo_image = TodoImage(
            todo_id=todo_id,
            filename=unique_filename,
            original_name=file.filename,
            file_path=file_path
        )
        db.add(todo_image)
        uploaded_files.append(todo_image)
    
    db.commit()
    
    # If it's an htmx request, return the updated image gallery
    if is_htmx_request(request):
        # Refresh the todo to get the updated images
        db.refresh(todo)
        return templates.TemplateResponse("partials/image_gallery.html", {
            "request": request,
            "todo": todo,
        })
    
    return RedirectResponse(url=f"/todo/{todo_id}", status_code=303)