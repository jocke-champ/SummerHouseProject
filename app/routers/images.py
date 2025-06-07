from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models import Todo, TodoImage
from app.dependencies import get_db
import os
import uuid
from pathlib import Path

router = APIRouter()

# Ensure uploads directory exists
os.makedirs("static/uploads", exist_ok=True)

@router.post("/api/todos/{todo_id}/images")
async def upload_image(
    todo_id: int,
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
    return RedirectResponse(url=f"/todo/{todo_id}", status_code=303)