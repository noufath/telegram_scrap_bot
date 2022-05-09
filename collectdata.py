from scrap.collect_customer import CollectCustomer
from scrap.collect_main_category import CollectMainCategory
from scrap.collect_product_item import CollectProductItems
from scrap.collect_sub_category import CollectSubCategory
from db_config.db_connect import Db_Connect
import applogger

def run(url_category, url_customer, db_connection):
    logger = applogger.AppLoger('info_log')

    logger.info("Start collecting data from shopee.co.id")
    
    CollectMainCategory(url_category, db_connection)
    CollectSubCategory(url_category, db_connection)
    CollectProductItems(db_connection)
    CollectCustomer(url_customer, db_connection)

    logger.info("Finished collecting data from shopee.co.id")
    


if __name__ == '__main__':
    urlcategories_target = 'https://shopee.co.id/api/v2/category_list/get_all'
    urlcustomer_shop = 'https://shopee.co.id/api/v4/product/get_shop_info?shopid='
    
    db = Db_Connect(limit_retries=5, reconnect= True)
       
    run(urlcategories_target, urlcustomer_shop, db)

    db.close()
 