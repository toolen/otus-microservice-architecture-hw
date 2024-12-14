from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session, init_db
from app.models import User, UserCreate


app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/users", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(first_name=user.first_name, last_name=user.last_name, id=user.id) for user in users]


@app.post("/users")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(first_name=user.first_name, last_name=user.last_name, id=user.id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user