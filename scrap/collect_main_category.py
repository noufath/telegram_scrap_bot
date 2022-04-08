import requests
from db_config.db_connect import Db_Connect
from string import Template
from applogger import AppLogger


class CollectMainCategory():

    def __init__(self, urlapi):
        self.urlapi = urlapi
        self.db = Db_Connect(limit_retries=5, reconnect= True)
        self.cursor = self.db._cursor
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
            
        self.db.close()
        AppLogger.info_log("Finished Collecting main category data")
            
#if __name__ == "__main__":
#   CollectMainCategory("https://shopee.co.id/api/v2/category_list/get_all")