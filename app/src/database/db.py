import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.conf.config import config
from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import ContactCreate, Contact, ContactUpdate   
from src import crud
from datetime import date, timedelta
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base, DatabaseSessionManager
from src.conf import settings
from src import crud


app = FastAPI()


SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(autocommit=False,
                                                                            autoflush=False,
                                                                            expire_on_commit=False,
                                                                            bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)



async def get_db():
    async with sessionmanager.session() as session:
        yield session

@app.post("/contacts/", response_model=Contact)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return crud.create_contact(db, contact)

@app.get("/contacts/", response_model=list[Contact])
async def get_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, updated_contact: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact = crud.update_contact(db, contact_id, updated_contact)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.delete("/contacts/{contact_id}", response_model=Contact)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = crud.delete_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact





@app.get("/contacts/search/", response_model=list[Contact])
async def search_contacts(
    query: str = Query(..., description="Search query for name, last name, or email"),
    db: AsyncSession = Depends(get_db)
):
    return crud.search_contacts(db, query)

@app.get("/contacts/birthdays/", response_model=list[Contact])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    return crud.get_upcoming_birthdays(db, today, next_week)



