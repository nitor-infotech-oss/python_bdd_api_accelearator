"""
This is the helper file for the REST API.
"""
from woocommerce import API
import logging as logger
import os
import requests.exceptions
from data_providers import logger_util
import logging
import json


class woo_request_helper(object):
    """
    This class implements the functionality to provide the connection to REST API
    by using REST API KEY and SECRET
    """
    __API_CONFIG_FILE = os.path.dirname(os.getcwd()) + '\\python_bdd_api_accelerator\\config\\api_config.json'

    def __init__(self):
        logs = logging.getLogger("root")
        logs.info("API Config File:" + self.__API_CONFIG_FILE)
        self.logger = logger_util.log_message(log_level="INFO", logger_name="root")

        with open(self.__API_CONFIG_FILE) as json_data:
            json_file = json.load(json_data)
        base_url = "http://mystore." + str(json_file["env"])

        if 'WC_KEY' in os.environ and 'WC_SECRET' in os.environ:
            wc_key = os.environ.get('WC_KEY')
            wc_secret = os.environ.get('WC_SECRET')
        else:
            wc_key = json_file["WC_KEY"]
            wc_secret = json_file["WC_SECRET"]

        self.wc_endpoint = None
        self.expected_status_code = None
        self.params = None
        self.rs = None
        self.wcapi = API(
            url=base_url,
            consumer_key=wc_key,
            consumer_secret=wc_secret,
            version="wc/v3"
        )

    def assert_status_code(self):
        """
        This function is used to verify the Response status code of API.
        """

        assert self.rs.status_code == self.expected_status_code, \
            "BAD STATUS CODE, EndPont: {}, Params: {}, Actual Status Code: {}, Expected Status code:{}".format(
                self.wc_endpoint, self.params, self.rs.status_code, self.expected_status_code)

    def assert_status_code_delete(self):
        """
        This function is used to verify the Response status code of Delete API.
        """
        assert self.rs.status_code == self.expected_status_code, \
            "BAD STATUS CODE, EndPont: {}, Actual Status Code: {}, Expected Status code:{}".format(self.wc_endpoint,
                                                                                                   self.rs.status_code,
                                                                                                   self.expected_status_code)

    def get_details(self, wc_endpoint, params=None, expected_status_code=200):
        """
        This function is used for GET API call.
        """
        self.rs = self.wcapi.get(wc_endpoint, params=params)

        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.params = params
        self.assert_status_code()

        return self.rs.json()

    def post_details(self, wc_endpoint, params=None, expected_status_code=201):
        """
        This function is used for POST API call.
        """
        self.logger.info("Params: {}".format(params))
        self.rs = self.wcapi.post(wc_endpoint, data=params)
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.params = params
        self.assert_status_code()

        return self.rs.json()

    def put_details(self, wc_endpoint, params=None, expected_status_code=200):
        """
        This function is used for PUT API call.
        """
        self.logger.info("Params: {}".format(params))
        self.rs = self.wcapi.put(wc_endpoint, data=params)
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.params = params
        self.assert_status_code()

    def delete_details(self, wc_endpoint, expected_status_code=200):
        """
        This function is used for DELETE API call.
        """
        self.rs = self.wcapi.delete(wc_endpoint, params={"force": True})
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.assert_status_code_delete()
