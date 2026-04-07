# app/models.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       server_default=text("now()"))

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    raw_input = Column(Text, nullable=False)  # plain English or JSON
    input_type = Column(String, nullable=False)  # "text" or "json"
    documentation = Column(Text)  # AI generated output
    owner_id = Column(Integer, ForeignKey("users.id",
                      ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       server_default=text("now()"))