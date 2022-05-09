from .tools import clearCatID, json_field, TextSanitize, toNumb
import requests
import json
import sys
from string import Template
import applogger


class CollectCustomer():

    def __init__(self, url, db_connection):
        self.db = db_connection
        self.cursor = self.db._cursor
        self.url = url
        
        self.GetCustomer()
    
    def GetCustomer(self):
        logger = applogger.AppLoger('info_log')

        strSQL = ("select distinct(shopid) shopid from item "
                "order by shopid asc;")
            
        self.cursor.execute(strSQL)

        _result = self.cursor.fetchall()

        for raw in _result:
            string_row = clearCatID(raw)
            
            self.CollectData(string_row)
            # click.echo('Saving customer id: {0}'.format(string_row))
            logger.info('Saving customer id: {0}'.format(string_row))
        
        self.db.close()

                
    def CollectData(self, _shopid):
        
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.73")
        header = {"User-Agent": UA}

        GetUrl = self.url + _shopid

        test_request = requests.get(GetUrl)
        if test_request.status_code == 200:
            resp = requests.get(GetUrl, headers=header).content.decode("utf-8")
            data = json.loads(resp)['data']
            
            list_field = list()
            list_val = list()
            

            # define field to be saved to database
            list_field = 'shopid', 'userid', 'last_active_time', \
                    'vacation', 'place', 'account',\
                    'is_shopee_verified', 'is_preferred_plus_seller',\
                    'is_official_shop', 'shop_location',\
                    'item_count', 'rating_star',\
                    'response_rate', 'session_info',\
                    'name', 'ctime', 'response_time',\
                    'follower_count', 'show_official_shop_label',\
                    'rating_bad', 'rating_good', 'rating_normal'

            list_val = data['shopid'], data['userid'], data['last_active_time'],\
                    data['vacation'], TextSanitize(data['place']), json_field(data['account']), data['is_shopee_verified'],\
                    data['is_preferred_plus_seller'], data['is_official_shop'], TextSanitize(data['shop_location']),\
                    toNumb(data['item_count']), toNumb(data['rating_star']), toNumb(data['response_rate']), json_field(data['session_info']),\
                    TextSanitize(data['name']), toNumb(data['ctime']), toNumb(data['response_time']), toNumb(data['follower_count']), data['show_official_shop_label'],\
                    toNumb(data['rating_bad']), toNumb(data['rating_good']), toNumb(data['rating_normal'])
            
            col_excluded = list(list_field)
            field = ''
            col_exc = ''
            i = 0
            for col in col_excluded:
                i += 1

                if i < len(col_excluded):
                    field += col + ", "
                    col_exc += col + "=EXCLUDED." + col + ", "
                else:
                    field += col
                    col_exc += col + "=EXCLUDED." + col
           
            Template_SQL = ("INSERT INTO customer ($fields_raw) VALUES $list_values"
                " ON CONFLICT (shopid) DO UPDATE SET $fields_excluded;\n"
            )

            strSQL = Template(Template_SQL).substitute(
                fields_raw= field,
                list_values=list_val,
                fields_excluded=col_exc
            )

            self.db.execute(strSQL)
           
            
        else:
            logger = applogger.AppLoger('error_log')
            # click.echo('Error server respon {}'.format(test_request.status_code))
            logger.error('Error server respon {}'.format(test_request.status_code))
            sys.exit(0)
