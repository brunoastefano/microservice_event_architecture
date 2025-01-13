import psycopg
import logging
from kafka import KafkaProducer
from json import dumps
from lib_order import Order
from db_log import DbLogHandler

def createOrder(order: Order, db_connector: psycopg.Connection, logger: logging.Logger):
  try:
    db_cursor = db_connector.cursor()

    db_cursor.execute('select create_order(%s,%s)', (order.customerId, order.total))
    db_connector.commit()
    result = db_cursor.fetchall()

    for row in result:
        order_id = row[0]
        order.setId(order_id)
    
    logger.info(f"Created | Order Id: {order.orderId}")

    for item in order.items:
      productId = item["productId"]
      quantity = item["quantity"]
      db_cursor.execute('select insert_order_item(%s,%s,%s)', (order.orderId, productId, quantity))
      db_connector.commit()
      logger.info(f"Inserted | Product Id {productId} | Order Id: {order.orderId}")

  except (Exception, psycopg.DatabaseError) as error:
    logger.exception(f"Unable to create order. {str(error)}")
    raise error

  finally:
    if db_connector:
      db_cursor.close()

def main(): 
  producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                          value_serializer=lambda x:dumps(x).encode('utf-8'),
                          retries=3,
                          max_block_ms = 1200000
                          )
  
  conn_string = "host='postgres' dbname='companydb' user='postgres' password='postgrespassword'"
  db_connector = psycopg.connect(conn_string)

  db_log_handler = DbLogHandler(db_connector)

  logging.getLogger('Producer').addHandler(db_log_handler)
  logger = logging.getLogger('Producer')
  logger.setLevel('DEBUG')

  order = Order(customerId = 1,
                items = [{"productId": "1", "quantity": 2}, {"productId": "2", "quantity": 1}],
                total = 150.00)
  

  createOrder(order, db_connector, logger)

  data = order.toJSON()

  producer.send('order.created', data)
  producer.flush()
  producer.close()

  logger.info(f"Published | order.created | OrderId: {order.orderId}")

  db_connector.close()

  print(data)

if __name__=="__main__":
  main()
