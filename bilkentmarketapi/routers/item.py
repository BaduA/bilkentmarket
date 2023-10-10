from typing import List
from uuid import uuid4
from fastapi import Form, UploadFile, status, HTTPException, Depends, APIRouter
from utlils import selected_clmn
import models
import schemas
import database
from sqlalchemy.orm import Session
from utlils import hash, verify
from . import oauth2
from validate_email import validate_email
import os
from fastapi_gcs import FGCSUpload, FGCSGenerate, FGCSDelete


router = APIRouter(prefix="/items", tags=["items"])
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = r"gcs/calm-athlete-392115-743705d981d7.json"

@router.get("/sell")
def get_selling_items(
    current_user=Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    return db.query(models.Item).filter(models.Item.seller.id == current_user.id).all()


@router.get("/bought")
def get_bought_items(
    current_user=Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    return db.query(models.Item).filter(models.Item.buyer.id == current_user.id).all()


@router.get("/{order}")
def get_items(
    order: int,
    db: Session = Depends(database.get_db),
):
    items = db.query(models.Item).all()
    if items.legth > order * 15:
        items = items[15 * (order - 1) : 15 * (order)]
    else:
        items = items[15 * (order - 1) :]
    return items


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    description: str = Form(""),
    name: str = Form(...),
    price: str = Form(...),
    categorynames: List[str] = Form([]),
    images: List[UploadFile] = Form(...),
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    print(categorynames)
    categories = []
    for ctg in categorynames:
        categories.append(
            db.query(models.Category)
            .filter(models.Category.categoryname == ctg)
            .first()
        )
    files = []
    for image in images:
        postname = uuid4().hex + ".jpg"
        files.append(models.Image(filename=postname))
        response = await FGCSUpload.file(
            project_id="calm-athlete-392115",
            bucket_name="bilkentmarketbucket",
            file=image,
            file_path=f"items/{name}",
            maximum_size=2_097_152,
            allowed_extension=["png", "jpg", "jpeg"],
            file_name=postname,
        )
    new_model = models.Item(
        name=name,
        description=description,
        price=price,
        seller=current_user,
        categories=categories,
        images=files,
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model


@router.put("/")
def update_item(
    reoffer: schemas.ReOffer,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    offer = db.query(models.Offer).filter(models.Offer.id == reoffer.offer_id)
    if not offer.first().filter(models.Offer.user_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You are not the offer owner",
        )
    if offer.first().offer_status == "INCREASE":
        if reoffer.new_price <= offer.price:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="You need to increase",
            )
    if offer.first().offer_status == "DENIED":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="This offer is denied",
        )
    offer.update({"price": reoffer.new_price})
    db.commit()
    return offer.first()


@router.put("/add_to_category")
def add_to_category(
    respond: schemas.OfferRespond,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    query_item = (
        db.query(models.Item).filter(models.Item.seller_id == current_user.id).first()
    )
    if not query_item:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You are not the item owner",
        )
    query_offer = db.query(models.Offer).filter(models.Offer.id == respond.offer_id)
    query_offer.update({"offer_status": respond.respond})
    db.commit()
    return query_offer.first()


@router.put("/{item_id}")
def hold_item(
    item_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    item = db.query(models.Item).filter(models.Item.id == item_id)
    if not item.first().filter(models.Item.seller.id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You are not the item owner",
        )
    item.update({"item_status": "ONHOLD"})
    db.commit()
    return item.first()
