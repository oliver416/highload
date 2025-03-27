from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import asyncio
import string
import random


DB_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def batch(query, list_: list[dict]) -> None:
    async with async_session() as db:
        await db.execute(query, list_)
        await db.commit()


if __name__ == '__main__':
    profiles = []
    letters = list(string.ascii_letters)
    query = text(
        'insert into profiles (name, age, sex) values (:name, :age, :sex);',
    )

    for i in range(10000):
        random.shuffle(letters) 
        name = ''.join(letters[0:10])
        age = random.randint(18, 100)
        sex = random.choice(('male', 'female'))
        profiles.append({'name': name, 'age': age, 'sex': sex})

    asyncio.run(batch(query, profiles))

    preferences = []
    query = text(
        f'''insert into preferences (id, min_age, max_age, sex) 
        values (:id, :min_age, :max_age, :sex);''',
    )

    for i in range(1, 10001):
        min_age = random.randint(18, 100)
        max_age = min_age + 10
        sex = random.choice(('male', 'female'))

        preferences.append({'id': i, 'min_age': min_age, 'max_age': max_age, 'sex': sex})

    asyncio.run(batch(query, preferences))

