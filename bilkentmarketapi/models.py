import database
from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Table,
    Float,
)
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


item_category = Table(
    "item_categories",
    database.Base.metadata,
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("item_name", ForeignKey("items.name")),
    Column("category_name", ForeignKey("categories.name")),
)


class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Item(database.Base):
    ITEM_STATUSES = (
        ("PENDING", "pending"),
        ("SELLED", "selled"),
        ("EXPIRED", "expired"),
    )
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    seller_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    buyer_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    item_status = Column(ChoiceType(choices=ITEM_STATUSES), default="PENDING")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Offer(database.Base):
    OFFER_STATUES = (
        ("PENDING", "pending"),
        ("ACCEPTED", "accepted"),
        ("DENIED", "denied"),
        ("INCREASE", "increase"),
        ("DECREASE", "decrease"),
    )
    __tablename__ = "offers"
    item_id = Column(
        Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    price = Column(Float, nullable=False)
    order_status = Column(ChoiceType(choices=OFFER_STATUES), default="PENDING")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Category(database.Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    categoryname = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
