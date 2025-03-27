from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import redis.asyncio as redis_client

import asyncio
import json
from collections import defaultdict


DB_URL = 'postgresql+asyncpg://postgres:postgres@postgresql:5432/postgres'

engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def main():
    redis = redis_client.Redis(host='redis', port=6379, decode_responses=True)

    async with async_session() as db:
        rows = await db.execute(text('select id from profiles;'))
        ids = tuple(i[0] for i in rows.all())

        rows = await db.execute(
            text(
                f'select id, min_age, max_age, sex ' 
                f'from preferences where id in {ids};',
            ),
        )
        prefs = rows.mappings().all()

        rows = await db.execute(text(
            '''SELECT id, ARRAY_AGG(blocked) AS blacklist
            FROM (
                SELECT id1 AS id, id2 AS blocked FROM swipes WHERE swipe1 = FALSE
                UNION ALL
                SELECT id2 AS id, id1 AS blocked FROM swipes WHERE swipe2 = FALSE
            ) _
            GROUP BY id;'''
        ))
        swipes = defaultdict(list)

        for i in rows.mappings().all():
            swipes[i['id']] = i['blacklist']

        for pref in prefs:
            rows = await db.execute(
                text(
                    f"""select * from profiles where """
                    f"""age between {pref['min_age']} and """
                    f"""{pref['max_age']} and sex='{pref['sex']}' """
                    f"""and id != ALL(:swipes);""",
                ),
                {'swipes': swipes[pref['id']]},
            )
            deck = json.dumps([dict(i) for i in rows.mappings().all()])
            await redis.set(f'deck|{pref["id"]}', deck)

    await redis.aclose()


async def run() -> None:
    while True:
        await main()
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(run())

