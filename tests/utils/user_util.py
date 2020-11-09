from data_providers import logger_util
from tests.utils import common
from helper.db_helpers import db_helpers
from data_providers.data_provider import DataProvider
from data_providers import json_parser
from data_providers import excel_util
import logging

logger = logging.getLogger("root")


class users(object):

    def __init__(self, context):
        self.db_helper = db_helpers()
        log_level = context.config.userdata.get('log_level')
        self.logger = logger_util.log_message(log_level, "root")
        self.random_email = None
        self.random_password = None
        self.user_id_from_gsheet = None
        self.payload = None
        self.user_email = None

    def get_user_by_email(self, email):
        """
        This function is used to get the user by email id from DataBase.

        :param email:
        :return:
        """
        sql = "SELECT * FROM local.wp_users where user_email = '{}';".format(email)
        return self.db_helper.execute_select(sql)

    def get_random_user(self):
        """
        This function is used to get random used from DataBase.

        :return:
        """
        sql = "SELECT * FROM local.wp_users WHERE ID > 3 ORDER BY RAND() limit 1;"
        return self.db_helper.execute_select(sql)

    def get_user_by_username(self, username):
        """
        This function is used to get user by username from DataBase.
        :param username:
        :return:
        """
        sql = "SELECT * FROM local.wp_users where user_login = '{}';".format(username)
        return self.db_helper.execute_select(sql)

    # -------------------------------------------------------GOOGLE SHEET----------------------------------------------#
    def create_user_by_gsheet(self, user):
        """
        This function is used to create a user from google sheet data.
        :param user:
        :return:
        """
        google_sheet_id = '1KWXC8u1baB_zl_JhC4BJiKL1JZTbB_uDljaIbx4FCNM'
        google_sheet = DataProvider(google_sheet_id=google_sheet_id)
        user_data = google_sheet.read_google_sheet_create_customer_api(user=user)
        self.payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        try:
            create_user_response = common.create_user(data=self.payload)

            if self.get_user_by_email(user_data['email']) is not None:
                logger.info("\n User Created Successfully")
            else:
                logger.info("\n User Creation failed")

            logger.info("\nUser ID: {}".format(create_user_response['id']))
            logger.info("\nUser Email: {}".format(create_user_response['email']))
            logger.info("\nUsername: {}".format(create_user_response['username']))

        except:
            logger.info("\nUser Already Exists !")

    def verify_customer_created_by_gsheet(self):
        """
        This function is used to verify the user created by google sheet.
        :return:
        """
        db_user = self.get_user_by_email(self.payload['email'])
        assert len(db_user) == 1, "Find User in DB by Email found {} results, EMAIL : {}".format(len(db_user),
                                                                                                 self.payload['email'])

        expected_username = self.payload['email'].split('@')[0]
        assert db_user[0]['user_login'] == expected_username, "Expected Username: {}, Actual Username: {}".format(
            expected_username, db_user[0]['user_login'])

    def delete_user_by_gsheet(self, username):
        """
        This function is used to delete a user by google sheet data.
        :param username:
        :return:
        """
        google_sheet_id = '1KWXC8u1baB_zl_JhC4BJiKL1JZTbB_uDljaIbx4FCNM'
        google_sheet = DataProvider(google_sheet_id=google_sheet_id)

        user_to_delete = google_sheet.read_google_sheet_delete_customer_api(username=username)
        user_data = self.get_user_by_email(email=user_to_delete['user_email'])

        try:
            self.user_id_from_gsheet = user_data[0]['ID']
            user_email = user_data[0]['user_email']
            logger.info("\n\tUSER DELETED: ")
            logger.info("\n\tUSER ID: {}".format(str(self.user_id_from_gsheet)))
            logger.info("\n\tUSERNAME {}".format(username))
            logger.info("\n\tUSER EMAIL {}".format(user_email))


        except:
            logger.info("\n\tUser {} Deleted or does not Exist!\n".format(username))

    def verify_user_deleted_by_gsheet(self, username):
        """
        This function is used to verify the user is deleted by google sheet data.
        :param username:
        :return:
        """
        try:
            return common.delete_user_by_id(user_id=self.user_id_from_gsheet)
        except:
            logger.info("\n\tUser {} Deleted or does not Exist!".format(username))

    # -------------------------------------------------------JSON----------------------------------------------#
    def create_user_by_json(self, user):
        """
        This function is used to create a user from json sheet data.
        :param user:
        :return:
        """
        filename = '../testdata/qa/python_bdd_api.json'
        user_data = json_parser.read_json_by_key(inputfile=filename, key=user)
        self.payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        try:
            create_user_response = common.create_user(data=self.payload)

            if self.get_user_by_email(user_data['email']) is not None:
                logger.info("\n User Created Successfully")
            else:
                logger.info("\n User Creation failed")

            logger.info("\nUser ID: {}".format(create_user_response['id']))
            logger.info("\nUser Email: {}".format(create_user_response['email']))
            logger.info("\nUsername: {}".format(create_user_response['username']))

        except:
            logger.info("\nUser Already Exists !")

    # -------------------------------------------------------EXCEL----------------------------------------------#

    def delete_user_by_xlsheet(self, username):
        """
        This function is used to delete a user by Excel sheet data.
        :param username:
        :return:
        """
        filename = 'tests\\testdata\\qa\\python_bdd_api.xlsx'
        sheetindex = 0
        user_to_delete = excel_util.get_sheet_data_into_hashmap(file_name=filename, sheet_index=sheetindex)[0][1]
        user_data = self.get_user_by_email(email=user_to_delete['user_email'])
        try:
            self.user_email = user_data[0]['user_email']
            logger.info("\n\tUSER DELETED: ")
            logger.info("\n\tUSERNAME {}".format(username))
            logger.info("\n\tUSER EMAIL {}\n".format(self.user_email))


        except:
            logger.info("\n\tUser {} Deleted or does not Exist!\n".format(username))

    def verify_user_deleted_by_xlsheet(self, username):
        """
        This function is used to verify the user is deleted by Excel sheet data.
        :param username:
        :return:
        """
        try:
            return self.get_user_by_email(email=self.user_email)
        except:
            logger.info("\n\tUser {} Deleted or does not Exist!".format(username))
