from multiprocessing.pool import ApplyResult
import psycopg2
import requests
from db_config.db_connect import Db_Connect
from string import Template
import applogger


class CollectMainCategory():

    def __init__(self, urlapi, db_connection):
        self.urlapi = urlapi
        self.db = db_connection
        self.SaveToDatabase(self.Collect_Main_Category())

    def Collect_Main_Category(self):
        url = self.urlapi
        resp = requests.get(url).json()
        category_source = resp["data"]

        
        list_values = list()
        for item in category_source:
            main_category = item.get("main")

            list_values += (main_category['display_name'], \
                    main_category['name'], \
                    main_category['catid'], \
                    main_category['parent_category'], \
                    str(main_category['is_adult']), \
                    str(main_category['block_buyer_platform']), \
                    main_category['sort_weight']),

        return list_values
        

    def SaveToDatabase(self, data):
        logger = applogger.AppLoger('info_log')

        cursor = self.db._cursor

        '''
        Template_SQL = ("INSERT INTO main_category(display_name,name,catid,parent_category,is_adult,block_buyer_platform, sort_weight) "
                            "VALUES $list_value "
                            "ON CONFLICT (catid) "
                            "DO UPDATE SET display_name=EXCLUDED.display_name, "
                            "name=EXCLUDED.name, parent_category=EXCLUDED.parent_category, "
                            "is_adult=EXCLUDED.is_adult, block_buyer_platform=EXCLUDED.block_buyer_platform, "
                            "sort_weight=EXCLUDED.sort_weight;"
            )
        
        for rec in data:
            strSQL = Template(Template_SQL).substitute(
                list_value=rec
            )
        
            self.db.execute(strSQL)
            logger.info("Saving main category : {}".format(rec))
        '''

        # change to use execute_mogrify for more speed saving data
      
        if data != []:
            format_string = '(' + ','.join(['%s', ]*len(data[0])) + ')\n'
            args_string = ','.join(cursor.mogrify(format_string, x).decode('utf-8') for x in data)
          
            str_SQL = ("INSERT INTO %s (display_name, name , catid , parent_category , is_adult, block_buyer_platform, sort_weight) VALUES " % ('main_category') + args_string + "ON CONFLICT (catid) "
                            "DO UPDATE SET display_name=EXCLUDED.display_name, "
                            "name=EXCLUDED.name, parent_category=EXCLUDED.parent_category, "
                            "is_adult=EXCLUDED.is_adult, block_buyer_platform=EXCLUDED.block_buyer_platform, "
                            "sort_weight=EXCLUDED.sort_weight;")
            
            try:
                self.db.execute(str_SQL)
            except (Exception, psycopg2.DatabaseError) as error:
                logger.info("Error: %s" % error)
                self.db._connection.rollback()
                cursor.close()
                return 1
            
            logger.info("Finished Collecting main category data")