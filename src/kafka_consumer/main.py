import psycopg
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from lib_order import Order

def applyDiscountToOrder(order: Order):
  discount = 10.0
  order.setDiscount(discount)

  db_connector = None
  try:
    conn_string = "host='localhost' dbname='companydb' user='postgres' password='postgrespassword'"
    db_connector = psycopg.connect(conn_string)
    db_cursor = db_connector.cursor()

    ################
    ### CALL DB FUNCTION TO UPDATE THE ORDER
  
  except (Exception, psycopg.DatabaseError) as error:
    raise error

  finally:
    if db_connector:
      db_cursor.close()
      db_connector.close()

def main(): 
  producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                          value_serializer=lambda x:dumps(x).encode('utf-8'),
                          retries=3
                          )

  consumer = KafkaConsumer(
    'order.created', 
    bootstrap_servers = ['localhost:9092'],
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'order',
    value_deserializer = lambda x : loads(x.decode('utf-8'))
    )

  for createdOrderMsg in consumer:
    print(type(createdOrderMsg.value))
    order = Order.initFromCreatedOrderJSON(createdOrderMsg.value)
    applyDiscountToOrder(order)

    data = order.toJSON()

    producer.send('order.processed', data)
    producer.flush()

if __name__=="__main__":
  main()

