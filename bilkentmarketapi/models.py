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


class Item(database.Base):
    ITEM_STATUSES = (
        ("PENDING", "pending"),
        ("SELLED", "selled"),
        ("EXPIRED", "expired"),
        ("ONHOLD", "onhold"),
    )
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    images = relationship("Image")

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    buyer_id = Column("buyer_id", ForeignKey("users.id"))
    seller_id = Column("seller_id", ForeignKey("users.id"))
    seller = relationship(
        "User", back_populates="selled_items", uselist=False, foreign_keys=[seller_id]
    )
    buyer = relationship(
        "User", back_populates="buyed_items", uselist=False, foreign_keys=[buyer_id]
    )
    item_status = Column(ChoiceType(choices=ITEM_STATUSES), default="PENDING")
    categories = relationship(
        "Category", secondary="item_categories", back_populates="items"
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


item_category = Table(
    "item_categories",
    database.Base.metadata,
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
    Column("item_id", ForeignKey("items.id"), primary_key=True),
)


class User(database.Base):
    USER_ROLES = (
        ("CUSTOMER", "customer"),
        ("ADMIN", "admin"),
    )
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone_num = Column(String, nullable=False)
    user_role = Column(ChoiceType(choices=USER_ROLES), default="CUSTOMER")
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    subcity = Column(String, nullable=False)
    school = Column(String, default="Bilkent University")
    department = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    rating = Column(Float, default=0)
    password = Column(String, nullable=False)
    buyed_items = relationship(
        "Item", back_populates="buyer", foreign_keys="Item.buyer_id"
    )
    selled_items = relationship(
        "Item", back_populates="seller", foreign_keys="Item.seller_id"
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Offer(database.Base):
    OFFER_STATUES = (
        ("PENDING", "pending"),
        ("ACCEPTED", "accepted"),
        ("DENIED", "denied"),
        ("INCREASE", "increase"),
        ("CANCELLED", "cancelled"),
    )
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    price = Column(Float, nullable=False)
    offer_status = Column(ChoiceType(choices=OFFER_STATUES), default="PENDING")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Category(database.Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    categoryname = Column(String, nullable=False)
    items = relationship(
        "Item", secondary="item_categories", back_populates="categories"
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Image(database.Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"))
