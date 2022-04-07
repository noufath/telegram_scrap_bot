import json
from tools import clearCatID
from db_connect import Db_Connect
from string import Template
import re
from collect_product_by_category import CollectProductByCategory
import click
import os
import sys


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
    
    click.echo('Scrap complete..!')
    sys.exit()
         

if __name__ == '__main__':
    CollectProductItems()