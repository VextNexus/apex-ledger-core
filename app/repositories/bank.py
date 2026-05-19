from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.bank import Account, Transaction
from app.schemas.bank import AccountCreate

class BankRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_account(self, account_data: AccountCreate) -> Account:
        db_account = Account(
            account_number = account_data.account_number,
            owner_name = account_data.owner_name,
            balance = account_data.balance
        )
        self.db.add(db_account)
        return db_account
    
    async def get_account(self, account_number: str) -> Account | None:
        query = select(Account).where(Account.account_number == account_number)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_transaction(self, sender: str, receiver: str, amount) -> Transaction:
        db_tx = Transaction(
            sender_account=sender,
            receiver_account=receiver,
            amount=amount
        )
        self.db.add(db_tx)
        return db_tx

