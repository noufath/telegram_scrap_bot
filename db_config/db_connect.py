import psycopg2
import time
from db_environ import Config
from applogger import AppLogger


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
               

    def connect(self, retry_counter=0):
        if not self._connection:
            try:
                self._connection = psycopg2.connect(**self.param_dict)
                retry_counter = 0
                self._connection.autocommit = False
                AppLogger.info_log('Database Connected')
                return self._connection

            except psycopg2.OperationalError as error:
                if not self.reconnect or retry_counter >= self.limit_retries:
                    raise error
                else:
                    retry_counter += 1
                    # print("Got Error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    AppLogger.error_log("Got Error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    time.sleep(5)
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                    raise error

    def pg_cursor(self):
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
            self._cursor = self._connection.cursor()

            return self._cursor

    def execute(self, str_query, retry_counter=0):
        try:
            self._cursor.execute(str_query)
            self._connection.commit()
            retry_counter = 0

        except:
            retry_counter += 1
            # print("Got Error {}. reconnecting {}".format(str_query, retry_counter))
            AppLogger.error_log("Got Error {}. reconnecting {}".format(str_query, retry_counter))
            time.sleep(1)
            self.reset()
            self.execute(str_query, retry_counter)
            self._connection.commit()

    def reset(self):
        self.close()
        self.connect()
        self.pg_cursor()

    def close(self):
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            # print('Database connection is closed')
            AppLogger.info_log('Database connection is closed')
        self._connection = None
        self._cursor = None

    def ignite(self):
        self.connect()
        self.pg_cursor()

Iginite = Db_Connect.ignite()