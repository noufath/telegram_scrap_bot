from multiprocessing.pool import ApplyResult
from string import Template
import psycopg2
import requests
from db_config.db_connect import Db_Connect
import json
from scrap.tools import TextSanitize
from string import Template
import applogger
import sys
import urllib.request

class CollectProductByCategory():

    def __init__(self, _catid, db_connection):
        self._catid = _catid
        
        self.url = ("https://shopee.co.id/api/v4/search/search_items?by=relevancy&limit=100"
            "&match_id={}&newest=0&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2").format(self._catid)

        
        self.db = db_connection
        
        self.SaveToDatabase(data=self.CollectProductCategory())
    

    def CollectProductCategory(self):
        
        UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.73")

        header = {"User-Agent": UA,
            'accept': '*/*',
            'accept-charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'accept-encoding': 'gzip, deflate, br',
            'connection': 'keep-alive',
            'cookie':'REC_T_ID=d56a3a4a-b6e2-11ec-b4a8-2cea7f475ec8; SPC_F=gveUkgVZZA4du9aSsig5jgkI1wmqy3z5;'
                '__LOCALE__null=ID; csrftoken=rbExzKmhGVhD2AOerAnzugHSONc7DCuZ; SPC_IA=-1; SPC_EC=-; SPC_U=-;'
                '_QPWSDCXHZQA=2f7530e0-340d-491b-aaa8-7d43bcaa41f6; _gcl_au=1.1.712926693.1649385454;'
                '_fbp=fb.2.1649385454503.1586246982; _gid=GA1.3.1800785616.1649385456; AMP_TOKEN=$NOT_FOUND;'
                'SPC_SI=21E8YgAAAABmZWdHWHpIMvWE5gAAAAAAY2dvam4xT0k=; _dc_gtm_UA-61904553-8=1; '
                'shopee_webUnique_ccd=9rHSqJO77U5myHoewmcGKQ==|+DK6OS8onrMyKq/mjjeK2eeJ+P1wlIYTenx7Fg+1Q23LgCpvEsRDvkqIzxSSS95q4w1QfKlxNEe0TcxP5GhFLw==|vfMq17xXzOui8K5q|04|3;'
                '_ga_SW6D8G0HXK=GS1.1.1649399253.3.1.1649401698.28; _ga=GA1.3.642674812.1649385455;' 
                'cto_bundle=DvqqsV9naHY0S01nUUpZdjFFa095dzZUOWVqVG1NV1ZweGlxUGNibzkySlZxZUpzeiUyQmJ5TnMzWHlBMUQlMkIxQjFCV0s4REhjOHJhM0VQd0NRUFZTa0doRWFqRFhGSzlTZDNIVDVzY29NViUyRmxEMW5YTkR1d1BRUTdZSzBkQ2ZPMjhZc1BiZw;'
                'SPC_T_IV="VM+npPE3Dw4m7/Xxp6Mpfg=="; SPC_T_ID="fOFUVKcxkbTfmFW2GCrUpfqvFCDG2Tgd/UqeDnLMCAZL4gO18N8HK3ZteimHUf/Luyg4TqNotzL9C8t2naPRArSvHqRqh62Ov43vKXugM14=";'
                'SPC_R_T_ID=fOFUVKcxkbTfmFW2GCrUpfqvFCDG2Tgd/UqeDnLMCAZL4gO18N8HK3ZteimHUf/Luyg4TqNotzL9C8t2naPRArSvHqRqh62Ov43vKXugM14=;'
                'SPC_R_T_IV=VM+npPE3Dw4m7/Xxp6Mpfg==; SPC_T_ID=fOFUVKcxkbTfmFW2GCrUpfqvFCDG2Tgd/UqeDnLMCAZL4gO18N8HK3ZteimHUf/Luyg4TqNotzL9C8t2naPRArSvHqRqh62Ov43vKXugM14=;'
                'SPC_T_IV=VM+npPE3Dw4m7/Xxp6Mpfg==',
            'x-shopee-language': 'id',
            'x-api-source': 'pc',
            'sec-fetch-mode': 'cors',
            'x-requested-with': 'XMLHttpRequest',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7,ms;q=0.6'
        }
        test_request = requests.get(self.url, headers=header)
        if test_request.status_code == 200:
            resp = requests.get(self.url, headers=header).content.decode("utf-8")
            _source = json.loads(resp)['items']
            
            list_rec = list()
       
           
            for data in _source:
               
                items = data['item_basic']


                # change null value to 0
                for key, val in items.items():
                    if val == 'null':
                        items.update({key: 0})

                    if val == "None":
                        items.update({key: None})
                
                    # None for jsonb data type
                    if key == 'label_ids' and val == None:
                        items.update({key: json.dumps(None)})

                    # change categoryid value using _catid's search parameter, because data got from scrap not related to master category
                    if key == 'catid':
                        items.update({key: self._catid})
            
                # create list record
                list_rec += (items['itemid'], items['shopid'], TextSanitize(items['name']), \
                    TextSanitize(items['label_ids']), items['image'], TextSanitize(items['images']), \
                    items['currency'], items['stock'], items['status'], \
                    items['ctime'], items['sold'], items['historical_sold'], \
                    items['liked'], items['liked_count'], TextSanitize(items['view_count']), \
                    TextSanitize(items['catid']), TextSanitize(items['brand']), items['cmt_count'], items['flag'], \
                    items['cb_option'], items['item_status'], items['price'], \
                    items['price_min'], items['price_max'], items['price_min_before_discount'], \
                    items['price_max_before_discount'], TextSanitize(items['hidden_price_display']), \
                    items['price_before_discount'], items['has_lowest_price_guarantee'], \
                    items['show_discount'], items['raw_discount'], TextSanitize(items['discount']), \
                    items['is_category_failed'], str(items['size_chart']),\
                    TextSanitize(str(items['item_rating'])), items['item_type'], \
                    items['reference_item_id'], items['transparent_background_image'], 
                    items['is_adult'], items['badge_icon_type'], items['shopee_verified'], \
                    items['is_official_shop'], items['show_official_shop_label'], items['show_shopee_verified_label'], \
                    items['show_official_shop_label_in_title'], items['is_cc_installment_payment_eligible'], \
                    items['is_non_cc_installment_payment_eligible'], TextSanitize(items['coin_earn_label']), items['show_free_shipping'], \
                    TextSanitize(items['preview_info']), TextSanitize(items['coin_info']), TextSanitize(items['exclusive_price_info']), TextSanitize(items['bundle_deal_id']), \
                    items['can_use_bundle_deal'], TextSanitize(items['bundle_deal_info']), TextSanitize(items['is_group_buy_item']), \
                    TextSanitize(items['has_group_buy_stock']), TextSanitize(items['group_buy_info']), items['welcome_package_type'], \
                    TextSanitize(items['welcome_package_info']), TextSanitize(items['add_on_deal_info']), items['can_use_wholesale'], \
                    items['is_preferred_plus_seller'], TextSanitize(items['shop_location']), items['has_model_with_available_shopee_stock'], \
                    TextSanitize(items['voucher_info']), items['can_use_cod'], items['is_on_flash_sale'], TextSanitize(items['spl_installment_tenure']), \
                    TextSanitize(items['is_live_streaming_price']), items['is_mart'], TextSanitize(items['pack_size'])),
          
            return list_rec
        else:
            
            logger = applogger.AppLoger('error_log')
            logger.error('Error server respon {}'.format(test_request.status_code))
            sys.exit(0)
      

    def SaveToDatabase(self, data):
        logger = applogger.AppLoger('info_log')
        cursor = self.db._cursor

        fields = ["itemid", "shopid", "name", "label_ids", "image", "images", "currency", "stock", "status", "ctime", "sold", "historical_sold", 
                "liked", "liked_count", "view_count", "catid", "brand", "cmt_count", "flag", "cb_option", "item_status", "price", "price_min",
                "price_max", "price_min_before_discount", "price_max_before_discount", "hidden_price_display", "price_before_discount",
                "has_lowest_price_guarantee", "show_discount", "raw_discount", "discount", "is_category_failed", "size_chart",
                "item_rating", "item_type", "reference_item_id", "transparent_background_image",
                "is_adult", "badge_icon_type", "shopee_verified", "is_official_shop", "show_official_shop_label", "show_shopee_verified_label",
                "show_official_shop_label_in_title", "is_cc_installment_payment_eligible", "is_non_cc_installment_payment_eligible", "coin_earn_label",
                "show_free_shipping", "preview_info", "coin_info",  "exclusive_price_info",  "bundle_deal_id",  "can_use_bundle_deal", "bundle_deal_info",
                "is_group_buy_item", "has_group_buy_stock", "group_buy_info", "welcome_package_type", "welcome_package_info", "add_on_deal_info", "can_use_wholesale",
                "is_preferred_plus_seller", "shop_location", "has_model_with_available_shopee_stock", "voucher_info", "can_use_cod", "is_on_flash_sale", "spl_installment_tenure",
                "is_live_streaming_price", "is_mart", "pack_size"]
        
        col = ''
        col_excluded = ''
        i = 0

        for field_name in fields:
            i += 1
            
            if i < len(fields):
                col += field_name + ", "
                col_excluded += field_name + "=EXCLUDED." + field_name + ", "
            else:
                col += field_name
                col_excluded += field_name + "=EXCLUDED." + field_name 
        
        Template_SQL = ("INSERT INTO item($fields_raw) VALUES $list_values"
            " ON CONFLICT (itemid) DO UPDATE SET $fields_excluded;\n"
        )

        # change to use mogrify for more speed saving

        '''
        for rec in data:

            strSQL = Template(Template_SQL).substitute(
                fields_raw=col, 
                list_values=rec,
                fields_excluded=col_excluded
            )

            
            self.db.execute(strSQL)
            
            logger.info('Saving data kode_produk: {0} - id_toko : {1} - nama_barang: {2}'.format(rec[0], rec[1], rec[2]))
        '''

        if data != []:
            format_string = '(' + ','.join(['%s', ]*len(data[0])) + ')\n'
            args_string = ','.join(cursor.mogrify(format_string, x).decode('utf-8') for x in data)

            strSQL = Template(Template_SQL).substitute(
                fields_raw=col, 
                list_values=args_string,
                fields_excluded=col_excluded
            )

            try:
                self.db.execute(strSQL)
            except (Exception, psycopg2.DatabaseError) as error:
                logger.info("Error %s" % error)
                self.db._connection.rollback()
                cursor.close()
                return 1
            
            logger.info("Finished Collecting product item in category: {}".format(self._catid))