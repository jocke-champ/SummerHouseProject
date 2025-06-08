from fastapi import APIRouter, HTTPException, Form, Depends, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models import ShoppingList, ShoppingItem
from app.dependencies import get_db
from typing import Optional
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/shopping", response_class=HTMLResponse)
async def shopping_home(request: Request, db: Session = Depends(get_db)):
    shopping_lists = db.query(ShoppingList).order_by(desc(ShoppingList.created_at)).all()
    return templates.TemplateResponse("shopping_index.html", {
        "request": request,
        "shopping_lists": shopping_lists
    })

@router.post("/api/shopping-lists")
async def create_shopping_list(
    name: str = Form(...),
    description: str = Form(""),
    created_by: str = Form(...),
    db: Session = Depends(get_db)
):
    shopping_list = ShoppingList(
        name=name,
        description=description,
        created_by=created_by
    )
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    return RedirectResponse(url="/shopping", status_code=303)

@router.get("/shopping/{list_id}")
async def get_shopping_list_detail(
    list_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Get items sorted by checked status, then by name
    items = db.query(ShoppingItem).filter(
        ShoppingItem.shopping_list_id == list_id
    ).order_by(ShoppingItem.is_checked, ShoppingItem.item_name).all()
    
    return templates.TemplateResponse("shopping_detail.html", {
        "request": request,
        "shopping_list": shopping_list,
        "items": items
    })

@router.post("/api/shopping-lists/{list_id}/items")
async def add_shopping_item(
    list_id: int,
    item_name: str = Form(...),
    quantity: float = Form(1.0),
    unit: str = Form("pcs"),
    notes: str = Form(""),
    added_by: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if list exists
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    item = ShoppingItem(
        shopping_list_id=list_id,
        item_name=item_name,
        quantity=quantity,
        unit=unit,
        notes=notes,
        added_by=added_by
    )
    db.add(item)
    db.commit()
    return RedirectResponse(url=f"/shopping/{list_id}", status_code=303)

@router.post("/api/shopping-items/{item_id}/toggle")
async def toggle_item_checked(
    item_id: int,
    checked_by: str = Form(...),
    db: Session = Depends(get_db)
):
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.is_checked = not item.is_checked
    if item.is_checked:
        item.checked_by = checked_by
        item.checked_at = datetime.utcnow()
    else:
        item.checked_by = None
        item.checked_at = None
    
    db.commit()
    return RedirectResponse(url=f"/shopping/{item.shopping_list_id}", status_code=303)

@router.post("/api/shopping-items/{item_id}/delete")
async def delete_shopping_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    list_id = item.shopping_list_id
    db.delete(item)
    db.commit()
    return RedirectResponse(url=f"/shopping/{list_id}", status_code=303)

@router.post("/api/shopping-lists/{list_id}/complete")
async def complete_shopping_list(
    list_id: int,
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    shopping_list.is_completed = True
    db.commit()
    return RedirectResponse(url="/shopping", status_code=303)

@router.get("/api/shopping-lists")
async def get_shopping_lists(db: Session = Depends(get_db)):
    return db.query(ShoppingList).order_by(desc(ShoppingList.created_at)).all()
