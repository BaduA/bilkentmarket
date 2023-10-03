from typing import List, Optional
from pydantic import BaseModel

# USER
class UserLogin(BaseModel):
    email: str
    password: str


class UserOut:
    username: str
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: str
    id:int
    password: str
    username: str
    phone_num: str
    name: str
    school:str = "Bilkent University"
    surname: str
    city: str
    subcity: str
    department: str
    grade: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserOut(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True


class ChangePsw(BaseModel):
    new_psw: str
    old_psw: str


# CATEGORY
class Category(BaseModel):
    name: str
    groupname: str


class CategoryOut(BaseModel):
    categoryname: str
    id: int


class DeleteCategory(BaseModel):
    id: int


class CategoryUpdate(BaseModel):
    id: int
    name: Optional[str]


# OFFER
class Offer(BaseModel):
    item_id: int
    price: int


class OfferRespond(BaseModel):
    offer_id: int
    respond: str


class ReOffer(BaseModel):
    offer_id: int
    new_price: int


# POST
class Item(BaseModel):
    name: str
    description: str
    price: float
    category_names: List[str]


class AddToCategories(BaseModel):
    category_names: List[str]
    item_id: int
