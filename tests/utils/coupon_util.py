from tests.utils import common
from helper.db_helpers import db_helpers
import logging
from data_providers import logger_util

logger = logging.getLogger("root")


class coupons(object):
    """
        This Class is used as coupon utility.
    """

    def __init__(self, context):
        log_level = context.config.userdata.get('log_level')
        self.logger = logger_util.log_message(log_level, "root")
        self.db_helper = db_helpers()
        self.new_coupon_info = None
        self.expected_discount_type = None
        self.data = None

    def get_coupon_by_id(self, coupon_id):
        """
        This function is used to return the coupon by coupon id from the DataBase.
        """

        sql = 'SELECT * FROM local.wp_posts where ID = {} AND post_type = "shop_coupon";'.format(coupon_id)

        return self.db_helper.execute_select(sql)

    def check_coupon_in_db(self, coupon_id):
        """
        This function is used to check for a coupon by coupon code in DataBase.
        """
        db_coupon = self.get_coupon_by_id(coupon_id)
        assert db_coupon, 'Coupon not found in DB, Coupon ID: {}'.format(coupon_id)

    def get_coupon_by_code(self, coupon_code):
        """
        This function is used to return the coupon by coupon code.
        :param coupon_code:
        :return:
        """
        sql = '''SELECT * FROM local.wp_posts where post_type = "shop_coupon" and post_title = '{}' '''.format(
            coupon_code)

        return self.db_helper.execute_select(sql)

    def create_coupon(self, discount_type=None, amount=None):
        """
        This function is used to create a coupon using api call.

        :param discount_type:
        :param amount:
        :return:
        """
        self.data = {
            "code": common.generate_random_coupon_code(),
        }

        if discount_type.lower() is not None:
            self.expected_discount_type = discount_type
            self.data["discount_type"] = discount_type
            self.data["amount"] = str(amount)

        else:
            self.expected_discount_type = 'fixed_cart'
            self.data["amount"] = str(amount)
        response_api = common.create_coupon(self.data)
        self.logger.info(
            "\nCoupon created with coupon id : {} and code : {}".format(response_api['id'], response_api['code']))
        self.new_coupon_info = response_api

    def verify_coupon(self):
        """
        This function is used to check for a coupon by coupon code in DataBase.
        :return:
        """
        self.get_coupon_by_code(coupon_code=self.data["code"])
