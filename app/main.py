import logging
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models.bank import Account, Transaction
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.bank import router as bank_router
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Старт приложения: Проверка и создание таблиц в БД...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблицы успешно проверены/созданы!")

    yield

    logger.info("Остановка приложения: Закрытие ресурсов...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version='1.0.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bank_router)

@app.get('/health')
async def health_chect():
    logger.info("Проверка состояния системы запрошена")
    return {
        "status": "operational",
        "project": settings.PROJECT_NAME
    }