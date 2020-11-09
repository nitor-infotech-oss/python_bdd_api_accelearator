# -*- coding: utf-8 -*-
from behave import *
from tests.utils.product_util import products


@step("I get number of available products from db")
def get_all_products_db(context):
    context.products = products(context)
    context.products.get_all_products_db()


@step("I get number of available products from API")
def get_all_products_api(context):
    context.products.get_all_products_api()


@step("the total number of products in API should be same as in DB")
def verify_total_products(context):
    context.products.verify_equal_db_api()


@step("I get {qty} random product from database")
def get_product_qty(context, qty):
    context.products = products(context)
    context.products.get_random_product_db(qty)


@step("I verify products api returns correct product by id")
def verify_correct_product(context):
    context.products.verify_get_correct_product_by_id()


@step("I update regular price of random products to {new_price}")
def update_price(context, new_price):
    context.products = products(context)
    context.products.update_price_of_random_product(price=new_price)


@step("verify price updated")
def verify_price_updated(context):
    context.products.verify_price_updated()
