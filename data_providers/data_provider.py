import os
import json
import logging
from faker import Faker
from data_providers.google_sheets_api import Workbook

faker = Faker()
LOGGER = logging.getLogger("root")


class DataProvider(object):
    """
    Data Provider class to build factory boy instances out of google sheets
    """

    def __init__(self, google_sheet_id):
        """
        Function to get admin settings based on agency and entity_id
        """
        self.google_sheet_id = google_sheet_id

        DEBUG = False
        exists = os.path.isfile('testdata.dict')
        if not DEBUG and not exists:

            csv_dict_temp = self.get_google_sheets_test_data()
            csv_dict = str(csv_dict_temp).strip()

            f = open('testdata.dict', 'w')
            f.write(csv_dict)
            f = open('testdata.dict', 'r')
            self.csv_dict = eval(f.read().strip())
            f.close()

        else:

            f = open('testdata.dict', 'r')
            csv_dict_existing = f.read()
            f.close()

            csv_dict_temp = self.get_google_sheets_test_data()
            csv_dict_new = str(csv_dict_temp).strip()

            if csv_dict_new != csv_dict_existing:

                f = open('testdata.dict', 'w')
                f.write(csv_dict_new)
                f = open('testdata.dict', 'r')
                self.csv_dict = eval(f.read().strip())
                f.close()

            else:

                f = open('testdata.dict', 'r')
                self.csv_dict = eval(f.read().strip())
                f.close()

    def get_object_from_string(self, key):
        """
        This function will return object(dict, list) from string x
        """
        obj = key
        try:
            if isinstance(key, basestring):
                obj = json.loads(key)
        except ValueError:
            return key
        return obj

    def get_google_sheets_test_data(self):
        """
        This function will return all googlesheets data in form of 3 dimensional array
        First index will be sheet name
        Second index will be profile type
        Third index will be column(header)
        Eg: profile_dict["client"]["client_with_no_contact"]["address"]
        will point to first row and address column of client sheet
        """
        csv_dict = {}
        csv_row = {}
        google_sheet = Workbook(spreadsheet_id=self.google_sheet_id)

        all_sheet_names = []
        for sheet in google_sheet.get_sheet_names():
            all_sheet_names.append(sheet['properties']['title'])

        for sheet_name in all_sheet_names:
            LOGGER.debug("Loading Sheet - {0}".format(sheet_name))
            all_rows = google_sheet.get_row_values(sheet_name)
            header_row = all_rows[0][1:]
            for i in range(1, len(all_rows)):
                row_val = all_rows[i]
                row_val = [self.get_object_from_string(val) for val in row_val]
                csv_row[row_val[0]] = dict(zip(header_row, row_val[1:]))
            csv_dict[sheet_name] = csv_row
            csv_row = {}
        return csv_dict

    def get_google_sheet_data_by_sheet_name(self, sheet_name=None):
        """
        his function will return google sheet data by sheet name
        """
        if sheet_name is None:
            return self.csv_dict
        else:
            try:
                sheet_data_by_sheet_name = self.csv_dict[sheet_name]
                return sheet_data_by_sheet_name
            except:
                print("SHEET NAME DOES NOT EXIST ")

    def get_google_sheet_data_by_row_num(self, sheet_name=None, row_num=None):
        """
        This function will return google sheet data by row number
        """
        google_sheet = Workbook(spreadsheet_id=self.google_sheet_id)

        if sheet_name is None:
            return self.get_google_sheets_test_data()

        elif sheet_name is not None and row_num is None:
            try:
                return self.get_google_sheet_data_by_sheet_name(sheet_name=sheet_name)
            except:
                print('Wrong Sheet Name is entered')
        else:
            try:
                return google_sheet.get_row_values(sheet_name=sheet_name, row_num=row_num)
            except:
                print("NO Data to retrieve")

    def get_google_sheet_id_by_sheet_name(self, sheet_name):
        """
        This function will return google sheet ID by Sheet Name
        """
        google_sheet = Workbook(spreadsheet_id=self.google_sheet_id)
        if sheet_name is None:
            return self.get_google_sheets_test_data()

        else:
            try:
                return google_sheet.get_sheet_id(sheet_name=sheet_name)
            except:
                print("Incorrect Sheet ID!")

    def get_all_google_sheet_names(self):
        """
        This function will return all google sheet names
        """
        google_sheet = Workbook(spreadsheet_id=self.google_sheet_id)

        sheet_names = []
        google_sheet_length = len(google_sheet.get_sheet_names())

        for i in range(0, google_sheet_length):
            sheet_names.append(google_sheet.get_sheet_names()[i]['properties']['title'])

        return sheet_names

    def get_all_google_sheet_details(self):
        """
        This function will return all google sheet details
        """
        google_sheet = Workbook(spreadsheet_id=self.google_sheet_id)

        return google_sheet.get_sheet_names()

    def read_google_sheet_create_customer_api(self, user):
        """
        This function will return username and password of the user
        """

        create_customer_dict = self.csv_dict['UsersApi_Create']

        try:
            return create_customer_dict[user]
        except:
            print("Failed to retrieve data for this user")

    def read_google_sheet_delete_customer_api(self, username):
        """
        This function will return username and password of the user
        """

        delete_customer_dict = self.csv_dict['UserApi_Delete']

        try:
            return delete_customer_dict[username]
        except:
            print("Failed to retrieve data for this user")

    def read_google_sheet_create_coupon_api(self, coupontype):
        """
        This function will return username and password of the user
        """

        create_coupon_dict = self.csv_dict['CouponApi_Create']

        try:
            return create_coupon_dict[coupontype]
        except:
            print("Failed to retrieve data for this user")
