from aiokafka import AIOKafkaConsumer
import asyncio


async def main():
    consumer = AIOKafkaConsumer(
        'test-topic',
        bootstrap_servers='localhost:9092',
        group_id='test-group',
    )
    await consumer.start()

    try:
        async for msg in consumer:
            print(f'Message: {msg.value.decode()}')
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(main())

