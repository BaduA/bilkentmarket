from fastapi import status, HTTPException, Depends, APIRouter
from utlils import selected_clmn
import models
import schemas
import database
from sqlalchemy.orm import Session
from utlils import hash, verify
from . import oauth2
from validate_email import validate_email

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_current_user(current_user=Depends(oauth2.get_current_user)):
    return selected_clmn([current_user], ["username", "email", "id"])[0]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_email = db.query(models.User).filter(models.User.email == user.email).first()
    user_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is an account with this email",
        )
    if user_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is an account with this username",
        )

    hashed_pw = hash(user.password)
    user.password = hashed_pw
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/change_psw")
def change_password(
    chg_psw: schemas.ChangePsw,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    isTrue = verify(chg_psw.old_psw, current_user.password)
    if isTrue:
        userQuery = db.query(models.User).filter(models.User.id == current_user.id)
        userQuery.update({"password": hash(chg_psw.new_psw)})
        db.commit()
        return "successfully changed password"
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="old password not matching",
        )


@router.put("/update")
def update_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    userQuery = db.query(models.User).filter(models.User.id == current_user.id)
    userQuery.update(user)
    db.commit()
    return userQuery.first()


@router.put("/changeUsername/{newUsername}")
def change_username(
    newUsername: str,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if current_user.username == newUsername:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="same as the old username",
        )
    if db.query(models.User).filter(models.User.username == newUsername).first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username taken"
        )
    db.query(models.User).filter(models.User.username == current_user.username).update(
        {"username": newUsername}
    )
    db.commit()
    return "success"


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return user
