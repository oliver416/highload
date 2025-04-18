from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text
import redis.asyncio as redis_client
import json
from fastapi.middleware.cors import CORSMiddleware


DB_URL = 'postgresql+asyncpg://postgres:postgres@postgresql:5432/postgres'

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

redis = redis_client.Redis(host='redis', port=6379, decode_responses=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class PreferenceRequest(BaseModel):
    id: int
    age: int
    sex: str


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


@app.post('/preferences')
async def create_preference(
    request: PreferenceRequest, 
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(text(
        f"""insert into preferences values 
        ({request.id}, {request.age}, '{request.sex}');""",
    ))
    await db.commit()
    return {'rows_affected': result.rowcount}


@app.get('/deck/{id}', response_model=list[ProfileResponse])
async def get_deck(id: int):
    deck = await redis.get(f'deck|{id}')
    return json.loads(deck)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        reload=True,
    )

