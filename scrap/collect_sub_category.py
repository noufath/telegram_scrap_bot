from os import environ
from sys import displayhook
import requests
from db_config.db_connect import Db_Connect
from string import Template
import re


class CollectSubCategory():

    def __init__(self, urlapi):
        self.urlapi = urlapi
        self.db = Db_Connect(limit_retries=5, reconnect= True)
        self.cursor = self.db._cursor
        self.SaveToDatabase(self.Collect_Sub_Category())
    
    def Collect_Sub_Category(self):
        url = self.urlapi
        resp = requests.get(url).json()
        _source = resp["data"]

        list_rec = list()
        for dt in _source:
            sub_category = dt.get('sub')
        
            for rec in sub_category:
                sub = str(rec['sub_sub'])
                sub_formated = sub.replace("\'","\"")
                sub_formated = sub_formated.replace("None","\"None\"")

                list_rec += (self.TextSanitize(str(rec['display_name'])), \
                    self.TextSanitize(str(rec['name'])), \
                    rec['catid'], \
                    rec['parent_category'], \
                    str(rec['is_adult']), \
                    str(rec['block_buyer_platform']), \
                    rec['sort_weight'],
                    sub_formated),

        return list_rec

    def TextSanitize(self, str):
        """Sanitizes a string so that it can be properly compiled in TeX.
        Escapes the most common TeX special characters: ~^_#%${}
        Removes backslashes.
        """
        s = re.sub('\\\\', '', str)
        s = re.sub(r'([_^$%&#{}])', r'\\\1', str)
        s = re.sub(r'\'', r'\\~{}', str)
        return s

    def SaveToDatabase(self, data):
        Template_SQL = ("INSERT INTO sub_category(display_name,name,catid,parent_category,is_adult,block_buyer_platform, sort_weight, sub_sub) "
                            "VALUES $list_recs "
                            "ON CONFLICT (catid) "
                            "DO UPDATE SET display_name=EXCLUDED.display_name, "
                            "name=EXCLUDED.name, parent_category=EXCLUDED.parent_category, "
                            "is_adult=EXCLUDED.is_adult, block_buyer_platform=EXCLUDED.block_buyer_platform, "
                            "sort_weight=EXCLUDED.sort_weight, "
                            "sub_sub=EXCLUDED.sub_sub;"
           )
        
        for rec in data:
            strSQL = Template(Template_SQL).substitute(
               list_recs=rec
            )
            
            self.db.execute(strSQL)
        
        self.db.close()
          

#if __name__ == "__main__":
#    CollectSubCategory("https://shopee.co.id/api/v2/category_list/get_all")