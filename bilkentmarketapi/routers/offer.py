from fastapi import status, HTTPException, Depends, APIRouter
import models
import schemas
import database
from sqlalchemy.orm import Session
from . import oauth2

router = APIRouter(prefix="/offers", tags=["users"])


@router.get("/")
def get_my_offers(
    current_user=Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    return db.query(models.Offer).filter(models.Offer.user_id == current_user.id).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_offer(
    offer: schemas.Offer,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if (
        db.query(models.Item).filter(models.Item.id == offer.id).first().item_status
        == "ONHOLD"
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Item is not for sale right now, its on hold",
        )
    if (
        db.query(models.Offer)
        .filter(models.Offer.user_id == current_user.id)
        .all()
        .lenght
        >= 4
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You have exceeded the limit of offers for this item",
        )
    model = models.Offer(
        user_id=current_user.id, price=offer.price, item_id=offer.item_id
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.put("/respond")
def respond_to_offer(
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


@router.put("/reoffer")
def reoffer(
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


@router.put("/{offer_id}")
def cancel_offer(
    offer_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id)
    if not offer.first().filter(models.Offer.user_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You are not the offer owner",
        )
    offer.update({"offer_status": "CANCELLED"})
    db.commit()
    return offer.first()
