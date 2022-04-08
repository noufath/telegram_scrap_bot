from scrap.collect_main_category import CollectMainCategory
from scrap.collect_product_item import CollectProductItems
from scrap.collect_sub_category import CollectSubCategory


def run(url_category):
    CollectMainCategory(url_category)
    CollectSubCategory(url_category)
    CollectProductItems()
    print("SELESAI")


if __name__ == '__main__':
    urlcategories_target = 'https://shopee.co.id/api/v2/category_list/get_all'
       
    run(urlcategories_target)
