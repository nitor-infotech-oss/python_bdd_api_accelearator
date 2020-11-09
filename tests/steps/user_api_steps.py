# -*- coding: utf-8 -*-
from behave import *
from tests.utils.user_util import users


@step("I create user {username}")
def create_user_google_sheet(context, username):
    context.users = users(context)
    context.users.create_user_by_gsheet(user=username)


@step("Verify user created")
def verify_create_user(context):
    context.users.verify_customer_created_by_gsheet()


@step("I create user")
def create_user_json(context):
    context.users = users(context)
    for row in context.table:
        context.users.create_user_by_json(user=row['username'])


@step("I Delete user {username}")
def delete_user_google_sheet(context, username):
    context.users = users(context)
    context.users.delete_user_by_gsheet(username=username)


@step("Verify user deleted {username}")
def verify_delete_user(context, username):
    context.users.verify_user_deleted_by_gsheet(username=username)


@step("I Delete user")
def delete_user_excel(context):
    context.users = users(context)
    for row in context.table:
        context.users.delete_user_by_xlsheet(username=row['username'])


@step("Verify user deleted")
def verify_delete_user(context):
    for row in context.table:
        context.users.verify_user_deleted_by_xlsheet(username=row['username'])


@step("Verify user created by step data")
@step("Verify user created by inline data")
def verify_user_create(context):
    pass

