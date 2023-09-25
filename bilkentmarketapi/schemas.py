from typing import List, Optional
from pydantic import BaseModel

# USER
class UserLogin(BaseModel):
    email: str
    password: str

class UserOut:
    username:str
    id:int

class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: str
    password: str
    username: str


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
    categoryname:str
    id:int

class DeleteCategory(BaseModel):
    id:int
    groupname: str


class CategoryUpdate(BaseModel):
    id: int
    name: Optional[str]
    post_ids: Optional[List[int]]


# GROUP
class Group(BaseModel):
    name: str
    members: Optional[list] = []

class JoinGroup(BaseModel):
    invToken: str
    groupName: str


class HandleReq(BaseModel):
    reqid: int
    owner_id:int
    is_accepted: bool



# POST
class PostOut(BaseModel):
    filename: str
    description: str
    owner_username: str
    id: int


class AddToCategory(BaseModel):
    post_ids: List[int]
    category_id: int

class CommentPost(BaseModel):
    comment:str
    groupname:str
    
class DeletePosts(BaseModel):
    post_ids:List[int]