from passlib.context import CryptContext

import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_psw, hashed_psw):
    return pwd_context.verify(plain_psw, hashed_psw)


def is_member(groupname, user, db):
    group = (
        db.query(models.Group).filter(models.Group.groupname == groupname).first()
    )
    groupid = group.id
    membership = (
        db.query(models.group_members)
        .filter(models.group_members.c.group_id == groupid)
        .filter(models.group_members.c.user_id == user.id)
        .first()
    )
    if not membership:
        return False
    else:
        return True

def selected_clmn(models, columns):
    new_models = []
    for model in models:
        new_model = {}
        for column in columns:
            new_model[column] = model.__dict__[column]
        new_models.append(new_model)
    return new_models