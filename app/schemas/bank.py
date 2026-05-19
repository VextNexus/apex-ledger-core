from pydantic import BaseModel, Field
from decimal import Decimal

class AccountCreate(BaseModel):
    account_number: str = Field(..., min_length=5, max_length=20, description="Уникальный номер счета")
    owner_name: str = Field(..., min_length=2, description="Имя владельца счета")
    balance: Decimal = Field(default=Decimal("0.0000"), ge=Decimal("0.0000"))

class AccountResponse(BaseModel):
    id: int
    account_number: str
    owner_name: str
    balance: Decimal
    model_config = {"from_attributes": True}

class TransferRequest(BaseModel):
    sender_account: str = Field(..., min_length=5, max_length=20)
    receiver_account: str = Field(..., min_length=5, max_length=20)
    amount: Decimal = Field(..., gt=Decimal("0.0000"), description=("Сумма Перевода"))

