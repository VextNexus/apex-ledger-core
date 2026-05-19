from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base
from decimal import Decimal

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, nullable=False, index=True)
    owner_name = Column(String, nullable=False)
    balance = Column(Numeric(precision=18, scale=4), nullable=False, default=Decimal("0.0000"))
    
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, index=True, primary_key=True)
    sender_account = Column(String, ForeignKey("accounts.account_number"), nullable=False)
    receiver_account = Column(String, ForeignKey("accounts.account_number"), nullable=False)
    amount = Column(Numeric(precision=18, scale=4), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
