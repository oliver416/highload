from confluent_kafka import Consumer

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'test-group',
})
consumer.subscribe(['test-topic'])

if __name__ == '__main__':
    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(f'{message.error()=}')
        else:
            print(f'Message has been received: {message.value().decode()}')

