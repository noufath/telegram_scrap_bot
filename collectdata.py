from scrap.collect_main_category import CollectMainCategory
from scrap.collect_product_item import CollectProductItems
from scrap.collect_sub_category import CollectSubCategory
from db_config.db_connect import Db_Connect
import applogger

def run(url_category, db_connection):
    logger = applogger.AppLoger('info_log')

    logger.info("Start collecting data from shopee.co.id")
    
    CollectMainCategory(url_category, db)
    CollectSubCategory(url_category, db)
    CollectProductItems(db)

    logger.info("Finished collecting data from shopee.co.id")
    


if __name__ == '__main__':
    urlcategories_target = 'https://shopee.co.id/api/v2/category_list/get_all'
    
    db = Db_Connect(limit_retries=5, reconnect= True)
       
    run(urlcategories_target, db)

    db.close()
