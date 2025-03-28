from confluent_kafka import Producer
import time
from datetime import datetime

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def callback(error, message):
    if error:
        print(f'{error=}')
    else:
        print(f'Message has sent to {message.topic()=}, {message.partition()=}')


if __name__ == '__main__':
    while True:
        label = datetime.now()
        producer.produce('test-topic', value=f'Test message: {label}', callback=callback)
        producer.flush()
        time.sleep(10)

