import logging
import psycopg

class DbLogHandler(logging.Handler):
  def __init__(self, db_connector: psycopg.Connection):
    logging.Handler.__init__(self)
    self.db_connector = db_connector

  def emit(self, record):
    log_msg = record.msg
    log_msg = log_msg.strip()
    log_msg = log_msg.replace('\'', '\'\'')

    print(self.db_connector.connection)


    with self.db_connector.cursor() as db_cursor:
      print("entered with")
      try:
        db_cursor.execute(f'select insert_log({record.levelno}, \'{record.levelname}\', \'{log_msg}\', \'{record.name}\')')
        self.db_connector.commit()

      except (Exception, psycopg.DatabaseError) as error:
        print("CRITICAL DB ERROR. Logging into DB is not possible.")
        raise error
    
    print("closed cursor")

