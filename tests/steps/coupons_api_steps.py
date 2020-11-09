# -*- coding: utf-8 -*-
from behave import *
from tests.utils.coupon_util import coupons


@step("I create a {discount_type} coupon with {amount}")
def create_coupon(context, discount_type, amount):
    context.coupons = coupons(context)
    context.coupons.create_coupon(discount_type, amount)


@step("coupon should be created")
def verify_coupon_created(context):
    context.coupons.verify_coupon()
