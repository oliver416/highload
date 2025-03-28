from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, text, Boolean, Integer
from aiokafka import AIOKafkaProducer

DB_URL = 'postgresql+asyncpg://postgres:postgres@postgresql:5432/postgres'

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()

app = FastAPI()


class SwipeRequest(BaseModel):
    swiper: int
    target: int
    decision: bool


@app.get('/')
def healthcheck() -> dict:
    return {'status': 'ok'}


@app.post('/swipe')
async def create_swipe(request: SwipeRequest, db: AsyncSession = Depends(get_db)):
    id1, id2 = sorted([request.swiper, request.target])
    decision = str(request.decision)
    values = [decision, 'null']
    num = 1

    if request.swiper == id2:
        num = 2
        values = ['null', decision]

    values = ','.join(values)

    async with db.begin():
        insert = await db.execute(text(
            f'''insert into swipes values ({id1},{id2}, {values}) on conflict do
            nothing;''',
        ))

        if insert.rowcount == 0:
            await db.execute(text(
                f'''update swipes set swipe{num}={decision} where id1={id1} 
                and id2={id2} and swipe{num} is null;'''
            ))
            row = await db.execute(text(
                'select (swipe1 and swipe2) from swipes where id1={id1} and id2={id2};'
            ))

            if row.one()[0] is True:
                producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')
                await producer.start()
                await producer.send_and_wait('notifications', '{id1}|{id2}'.encode())
                await producer.stop()


    return {'rows_affected': insert.rowcount}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        reload=True,
    )

