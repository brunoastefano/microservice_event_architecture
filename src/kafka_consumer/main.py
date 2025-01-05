from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'quickstart-events', 
    bootstrap_servers = ['localhost:9092'],
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'quickstart-events-consumer',
    value_deserializer = lambda x : loads(x.decode('utf-8'))
    )

for message in consumer:
    print(message.value)
