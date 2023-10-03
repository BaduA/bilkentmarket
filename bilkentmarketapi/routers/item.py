from fastapi import status, HTTPException, Depends, APIRouter
from utlils import selected_clmn
import models
import schemas
import database
from sqlalchemy.orm import Session
from utlils import hash, verify
from . import oauth2
from validate_email import validate_email

router = APIRouter(prefix="/items", tags=["users"])


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
def create_item(
    item: schemas.Item,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    categories = []
    for ctg in item.category_names:
        categories.append(
            db.query(models.Category)
            .filter(models.Category.categoryname == ctg)
            .first()
        )
    new_model = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        seller=current_user,
        categories=categories,
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
