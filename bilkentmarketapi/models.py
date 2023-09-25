import database
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.sql.expression import text

class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )