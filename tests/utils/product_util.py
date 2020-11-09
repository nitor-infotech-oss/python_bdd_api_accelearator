from helper.db_helpers import db_helpers
from tests.utils import common
import logging
import random
from data_providers import logger_util

logger = logging.getLogger("root")


class products(object):
    """
        This Class is used for API operations on products.
    """

    def __init__(self, context):
        self.db_helper = db_helpers()
        log_level = context.config.userdata.get('log_level')
        self.logger = logger_util.log_message(log_level, "root")
        self.qty_products_db = None
        self.qty_products_api = None
        self.random_products = None
        self.payload = None
        self.random_product_id = None

    def update_price_of_random_product(self, price=None):
        """
        This function is used to update the product price of random products.

        :param price:
        :return:
        """
        qty = 1

        if str(price) is None:
            self.payload = {
                "regular_price": "50"
            }
        else:
            self.payload = {
                "regular_price": str(price)
            }
        self.random_products = self.get_random_products_from_db(qty)
        self.random_product_id = self.random_products[0]['ID']
        product_name = self.random_products[0]['post_title']

        logger.info("ProductPage ID: " + str(self.random_product_id))
        logger.info("ProductPage Name: " + product_name)
        logger.info("New Price : " + self.payload["regular_price"])

    def get_all_products_from_db(self):
        """
        This function is used to get number of all the products from DataBase.
        """
        sql = "SELECT * FROM local.wp_posts where post_type = 'product';"
        rs_sql = self.db_helper.execute_select(sql)
        return rs_sql

    def get_random_products_from_db(self, qty):
        """
        This function is used to get random products from the DataBase.
        """
        sql = "SELECT * FROM local.wp_posts where post_type = 'product' order by id desc limit 5000;"
        rs_sql = self.db_helper.execute_select(sql)

        return random.sample(rs_sql, int(qty))

    def get_product_by_id(self, product_id):
        """
        This function is used to get the product by product ID
        """
        try:
            product = common.get_products_by_id(product_id)
            self.logger.info("\n\tGetting Product by ID:{}\n\tProduct Name: {}".format(product_id, product['name']))
            return common.get_products_by_id(product_id)
        except TypeError:
            pass

    def get_all_products_db(self):
        """
        This function is used to get all the products from the DataBase.
        """
        self.qty_products_db = len(self.get_all_products_from_db())
        self.logger.info("Number of Products in DB : {}".format(self.qty_products_db))

    def get_all_products_api(self):
        """
        This function is used to get all the products from API.
        """
        self.qty_products_api = len(common.list_all_products())
        self.logger.info("\n\tTotal Number of Products is : {}\n\t".format(self.qty_products_api))

    def verify_equal_db_api(self):
        """
        This function is used to verify the number of products in DB and API are equal.
        """
        assert self.qty_products_api == self.qty_products_db, "The Number of Products in DB and API response do not match. DB qty: {}, API qyt: {}".format(
            self.qty_products_db, self.qty_products_api)

    def get_random_product_db(self, qty):
        """
        This function is used to return random products from DataBase.
        """
        self.random_products = self.get_random_products_from_db(qty)

    def verify_get_correct_product_by_id(self):
        """
        This function is used to get correct product by Product ID.
        """
        product_id = self.random_products[0]['ID']
        rs_get_product = common.get_products_by_id(product_id)

        assert rs_get_product['id'] == product_id, "Wrong ProductPage ID when calling 'get product by id'"
        assert rs_get_product['name'] == self.random_products[0][
            'post_title'], "Wrong ProductPage name when calling 'get product by id'. API: {} DB: {}".format(
            rs_get_product['name'], self.random_products[0]['post_title'])

    def verify_price_updated(self):
        """
        This function is used to verify that the product price is updated.
        """
        return common.update_random_product_price(product_id=self.random_product_id, data=self.payload)

    def get_random_products_by_qty(self, qty):
        """
        This function is used to get the random products by quantity.
        """
        for i in range(0, qty):
            product = self.get_random_products_from_db(qty)[i]
            self.logger.info("\nProduct ID: {} \t Product Name: {}".format(product['ID'], product['post_title']))
