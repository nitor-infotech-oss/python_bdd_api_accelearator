"""
    This file is used as Database utility
    - for creating or establishing DataBase connection.
    - executing sql queries on orders, products, and users table.
"""
import pymysql
import os
import json
import logging

logger = logging.getLogger("root")


class db_helpers(object):
    """
        This Class provides the functionality to
        establish the connection to DataBase using the config file and
        all the functions related to database
    """
    __DB_CONFIG_FILE = os.path.dirname(os.getcwd()) + '\\python_bdd_api\\config\\db_config.json'

    def __init__(self):
        logger.info("DB Config File:" + self.__DB_CONFIG_FILE)
        with open(self.__DB_CONFIG_FILE) as json_data:
            json_file = json.load(json_data)

        if 'DB_USER' in os.environ and 'DB_PASSWORD' in os.environ:
            self.db_user = os.environ.get('DB_USER')
            self.db_password = os.environ.get('DB_PASSWORD')
        else:
            self.db_user = json_file["username"]
            self.db_password = json_file["password"]
        self.host = json_file["host"]
        self.port = json_file["port"]

        self.connection = None

    def create_connection(self):
        """
        This function is used to establish a DataBase connection.
        """

        self.connection = pymysql.connect(host=self.host, port=self.port, user=self.db_user, password=self.db_password)

    def execute_select(self, sql):
        """
        This function is used to execute a select command.
        """

        try:
            self.create_connection()
            cur = self.connection.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception("Failed running SQL {}. Error: {}".format(sql, str(e)))
        finally:
            self.connection.close()

        return rs_dict
