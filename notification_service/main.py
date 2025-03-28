from aiokafka import AIOKafkaConsumer
import asyncio
from loguru import logger


async def main():
    consumer = AIOKafkaConsumer(
        'notifications',
        bootstrap_servers='kafka:9092',
        group_id='group-i',
    )
    await consumer.start()

    try:
        async for msg in consumer:
            id1, id2 = msg.value.decode().split('|')
            logger.info(f'Profile {id1} has swiped profile {id2}')
            logger.info(f'Profile {id2} has swiped profile {id1}')
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(main())

