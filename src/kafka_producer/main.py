import psycopg
from kafka import KafkaProducer
from json import dumps
from lib_order import Order

def createOrder(order: Order):
  db_connector = None
  try:
    conn_string = "host='localhost' dbname='companydb' user='postgres' password='postgrespassword'"
    db_connector = psycopg.connect(conn_string)
    db_cursor = db_connector.cursor()

    db_cursor.execute('select create_order(%s,%s)', (order.customerId, order.total))
    db_connector.commit()
    result = db_cursor.fetchall()

    for row in result:
        order_id = row[0]
        order.setId(order_id)

    for item in order.items:
      db_cursor.execute('select insert_order_item(%s,%s,%s)', (order.orderId, item["productId"], item["quantity"]))
      db_connector.commit()

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

  order = Order(customerId = 1,
                items = [{"productId": "1", "quantity": 2}, {"productId": "2", "quantity": 1}],
                total = 150.00)

  createOrder(order)

  data = order.toJSON()

  producer.send('order.created', data)
  producer.flush()
  producer.close()

  print(data)

if __name__=="__main__":
  main()
