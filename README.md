# Microservice Event Architecture
This project implements a simple microservice event architecture for a ordering system. 

## Producer
A producer service creates an order by instantiating a Order object and persisting it to the database, when it acquires an order id. The producer service then publishes the created order on the order.created topic in the Kafka broker. The order serialization is handled by the toJSON method of the Order class.

## Consumer
A consumer service reads an order from the order.created topic in the Kafka broker and instantiates on Order object with the recceived order. A discount is applied to the order, handled by the Order class, and the processed order is persisted in the database. The consumer then publishes the order in the order.processed topic. The order serialization is handled by the toJSON method of the Order class.

## Logger
The db_log.py file contains an implementation of a log handler that logs into the database.

## Order
The lib_order.py file contains the implementation of order related classes and methods.

## Running the system
1 - Clone this git repository 
```
git clone https://github.com/brunoastefano/microservice_event_architecture.git
```
2 - Go to the repository folder and run with docker compose
```
docker compose up
```

## Useful commands
Create kafka topic 
```
docker exec -it <container-id> /opt/kafka/bin/kafka-topics.sh --create --topic <topic-name> --bootstrap-server localhost:9092
```

Open publisher to kafka topic
```
docker exec -it <container-id> /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic <topic-name>
```

Open publisher to kafka topic
```
docker exec -it <container-id> /opt/kafka/bin/kafka-console-consumer.sh --topic <topic-name> --from-beginning --bootstrap-server localhost:9092
```

### Navigating into PostgreSQL
*`docker ps` To list the containers
*`docker exec -it <container-id> bash` To open the bash for the postgres container
*`psql -U postgres` To log into DB environment
*`\c companydb` To connect into the companydb database (Change the name of the database if needed)
*`\dt` To list all tables
*`select * from table "order";` To list all active orders in table order

## Stack 
*Data Base -> PostgreSQL
*Event Broker -> Kafka
*Services -> Python
