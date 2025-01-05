from kafka import KafkaProducer 
from json import dumps

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda x:dumps(x).encode('utf-8')
                        )

data = """{
  "orderId": "12345",
  "customerId": "67890",
  "items": [
    {"productId": "A1", "quantity": 2},
    {"productId": "B2", "quantity": 1}
  ],
  "total": 150.00
}"""

producer.send('quickstart-events', data)
producer.flush()
