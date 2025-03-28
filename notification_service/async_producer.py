import asyncio
from aiokafka import AIOKafkaProducer
from datetime import datetime


async def main():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    try:
        while True:
            await producer.send_and_wait(
                'test-topic', 
                f'Test message: {datetime.now()}'.encode(),
            )
            print('Message has been sent')
            await asyncio.sleep(10)
    finally:
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(main())

