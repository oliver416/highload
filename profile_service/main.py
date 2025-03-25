from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text

DB_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)

app = FastAPI()


class ProfileRequest(BaseModel):
    name: str
    age: int
    sex: str


class ProfileResponse(BaseModel):
    id: int
    name: str
    age: int
    sex: str

    class Config:
        from_attributes = True


@app.get('/')
def healthcheck() -> dict:
    return {'status': 'ok'}


@app.get('/profile')
async def get_profiles(db: AsyncSession = Depends(get_db)) -> list[ProfileResponse]:
    result = await db.execute(text('select * from profiles;'))
    return result.mappings().all()


@app.post('/profile', response_model=ProfileResponse)
async def create_profile(request: ProfileRequest, db: AsyncSession = Depends(get_db)):
    profile = Profile(**request.dict())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port=8000,
        log_level='info',
        reload=True,
    )

