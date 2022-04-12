import json
from scrap.tools import clearCatID
from db_config.db_connect import Db_Connect
from string import Template
import re
from scrap.collect_product_by_category import CollectProductByCategory
import applogger


class CollectProductItems():

    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db._cursor
       

        self.GetItems()

    def GetItems(self):
        logger = applogger.AppLoger('info_log')

        strSQL = ("select distinct(catid) from main_category mc "
                    " union "
                    "select distinct(catid) from sub_category sc ")

        self.cursor.execute(strSQL)

        _result = self.cursor.fetchall()
    
        for raw in _result:
            string_row = clearCatID(raw)
            CollectProductByCategory(string_row, self.db)
    
        logger.info("Finished collecting product item")
        self.db.close()