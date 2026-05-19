import logging
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from app.repositories.bank import BankRepository
from app.schemas.bank import AccountCreate, TransferRequest

logger = logging.getLogger(__name__)

class BankService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = BankRepository(db)

    async def create_new_account(self, account_data: AccountCreate):
        existing = await self.repo.get_account(account_data.account_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Счет с таким номером уже существует"
            )
        account = await self.repo.create_account(account_data)
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def transfer_money(self, transfer_data: TransferRequest):
        amount = Decimal(str(transfer_data.amount))

        async with self.db.begin():
            await self.db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            try:
                sender = await self.repo.get_account(transfer_data.sender_account)
                if not sender:
                    raise HTTPException(status_code=404, detail="Счет отправителя не найден")

                receiver = await self.repo.get_account(transfer_data.receiver_account)
                if not receiver:
                    raise HTTPException(status_code=404, detail="Счет получателя не найден")

                if sender.account_number == receiver.account_number:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Нельзя переводить деньги на тот же счет",
                    )

                sender_balance = Decimal(str(sender.balance))
                if sender_balance < amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Insufficient funds",
                    )

                sender.balance = sender_balance - amount
                receiver.balance = Decimal(str(receiver.balance)) + amount

                await self.repo.create_transaction(
                    sender=sender.account_number,
                    receiver=receiver.account_number,
                    amount=amount,
                )

                logger.info(
                    "Успешный перевод %s со счета %s на %s",
                    amount,
                    sender.account_number,
                    receiver.account_number,
                )

                return {
                    "message": "Перевод успешно выполнен",
                    "amount": str(amount),
                }

            except DBAPIError as e:
                if "40001" in str(e.orig):
                    logger.warning(
                        "Конфликт Serializable транзакции. Запрос заблокирован базой данных."
                    )
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Система перегружена параллельными запросами. Пожалуйста, повторите операцию.",
                    ) from e
                raise
