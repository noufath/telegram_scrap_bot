import json
from scrap.tools import clearCatID
from db_config.db_connect import Db_Connect
from string import Template
import re
from scrap.collect_product_by_category import CollectProductByCategory
from applogger import AppLogger


class CollectProductItems():

    def __init__(self):
        self.db = Db_Connect(limit_retries=5, reconnect=True)
        self.cursor = self.db._cursor
        

        self.GetItems()

    def GetItems(self):
        strSQL = ("select distinct(catid) from main_category mc "
                    " union "
                    "select distinct(catid) from sub_category sc ")

        self.cursor.execute(strSQL)

        _result = self.cursor.fetchall()
    
        for raw in _result:
            string_row = clearCatID(raw)
            CollectProductByCategory(string_row)
    
    AppLogger.info_log("Finished collecting product item")
         

# if __name__ == '__main__':
#    CollectProductItems()