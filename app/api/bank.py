from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.bank import BankService
from app.schemas.bank import TransferRequest, AccountResponse, AccountCreate

router = APIRouter(prefix="/bank", tags=["Bank Operation"])
@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)

async def create_account(account_data: AccountCreate, db: AsyncSession = Depends(get_db)):
    service = BankService(db)
    return await service.create_new_account(account_data)

@router.post("/transfer", status_code=status.HTTP_200_OK)
async def transfer_money(transfer_data: TransferRequest, db: AsyncSession = Depends(get_db)):
    service = BankService(db)
    return await service.transfer_money(transfer_data)
