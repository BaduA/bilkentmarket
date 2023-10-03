from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database, schemas, models, utlils
from .oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_creds: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User).filter(models.User.email == user_creds.username).first()
    )

    if not user:
        user = (
            db.query(models.User)
            .filter(models.User.phone_num == user_creds.username)
            .first()
        )
        if not user:
            user = (
                db.query(models.User)
                .filter(models.User.id == user_creds.username)
                .first()
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="No users matched"
                )

    isUser = utlils.verify(user_creds.password, user.password)

    if isUser:
        access_token = create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Password"
        )
