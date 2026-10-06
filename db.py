from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import os

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = "localhost"
DB_PORT = 5431

DB_DSN = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DB_DSN)
DbSession = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiCharacters(Base):
    __tablename__ = "swapi_characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String)
    eye_color: Mapped[str] = mapped_column(String)
    films: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    hair_color: Mapped[str] = mapped_column(String)
    height: Mapped[str] = mapped_column(String)
    homeworld: Mapped[str] = mapped_column(String)
    mass: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    skin_color: Mapped[str] = mapped_column(String)
    starships: Mapped[str] = mapped_column(String)
    vehicles: Mapped[str] = mapped_column(String)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()

