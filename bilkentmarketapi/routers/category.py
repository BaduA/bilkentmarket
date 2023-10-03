from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from utlils import is_member
import models
import database
import schemas
from sqlalchemy.orm import Session
from . import oauth2

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/create")
async def create_category(
    model: schemas.Category,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not is_member(model.groupname, current_user, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not a member"
        )
    group = (
        db.query(models.Group).filter(models.Group.groupname == model.groupname).first()
    )
    if group.categories.filter(models.Category.categoryname == model.name).first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="your group has a category named this",
        )
    group_id = group.id
    category_model = models.Category(categoryname=model.name, group_id=group_id)
    db.add(category_model)
    db.commit()
    db.refresh(category_model)
    return category_model

@router.put("/update")
async def update_category(
    model: schemas.CategoryUpdate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if current_user.user_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not an admin"
        )
    query = db.query(models.Category).filter(models.Category.id == model.id)
    if model.name:
        query.update({"categoryname": model.name})
    db.commit()
    return query.first()


@router.delete("/delete")
async def delete_category(
    model: schemas.DeleteCategory,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if current_user.user_role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not an admin"
        )
    category = db.query(models.Category).filter(models.Category.id == model.id)
    if category.first().categoryname == "All":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="cant delete All"
        )
    category.delete(
        synchronize_session=False
    )
    db.commit()
    return "success"
