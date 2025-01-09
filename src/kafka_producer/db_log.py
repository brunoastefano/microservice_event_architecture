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

    try:
      db_cursor = self.db_connector.cursor()
      db_cursor.execute(f'select insert_log({record.levelno}, \'{record.levelname}\', \'{log_msg}\', \'{record.name}\')')
      self.db_connector.commit()

    except (Exception, psycopg.DatabaseError) as error:
      print("CRITICAL DB ERROR. Logging into DB is not possible.")
      raise error

    finally:
      if self.db_connector:
        db_cursor.close()

