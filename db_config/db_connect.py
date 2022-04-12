import psycopg2
import time
from db_config.db_environ import Config
import applogger


class Db_Connect():
    def __init__(self, limit_retries, reconnect):
        self.param_dict = {
            "host": Config.POSTGRES_HOST,
            "port": Config.POSTGRES_PORT,
            "database": Config.POSTGRES_DB,
            "user": Config.POSTGRES_USER,
            "password": Config.POSTGRES_PASSWORD
        }

        self._connection = None
        self._cursor = None
        self.reconnect = reconnect
        self.limit_retries = limit_retries
        self.ignite()     

    def connect(self, retry_counter=0):
        
        if not self._connection:
            try:
                self._connection = psycopg2.connect(**self.param_dict)
                retry_counter = 0
                self._connection.autocommit = False
                logger = applogger.AppLoger('info_log')
                logger.info('Database Connected')
                return self._connection

            except psycopg2.OperationalError as error:
                
                if not self.reconnect or retry_counter >= self.limit_retries:
                    logger = applogger.AppLoger('info_log')
                    logger.info("failed to connect to database. {} times failed to attempt connection".format(retry_counter))
                    raise error
                else:
                    logger = applogger.AppLoger('error_log')
                    retry_counter += 1
                    
                    logger.error("Got Error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    time.sleep(5)
                    
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                    raise error

    def pg_cursor(self):
        logger = applogger.AppLoger('info_log')
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
                logger.info("pg_cursor created")

            self._cursor = self._connection.cursor()

            return self._cursor

    def execute(self, str_query, retry_counter=0):
        logger = applogger.AppLoger('info_log')
        try:
            self._cursor.execute(str_query)
            self._connection.commit()
            retry_counter = 0

        except:
            retry_counter += 1
            logger.error("Got Error {}. reconnecting {}".format(str_query, retry_counter))
            time.sleep(1)
            
            self.reset()

            # Try execute query after reseting connection
            self.execute(str_query, retry_counter)
            self._connection.commit()

    def reset(self):
        logger = applogger.AppLoger('info_log')
        self.close()
        
        self.ignite()
        logger.info("Connection has been reset")

    def close(self):
        logger = applogger.AppLoger('info_log')
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            
            logger.info('Database connection is closed')
        self._connection = None
        self._cursor = None

    def ignite(self):
        self.connect()
        self.pg_cursor()

