# -*- coding: utf-8 -*-
@api @user_api_create
Feature: UserCreate API Smoke

  @create_user_api
  Scenario Outline: Verify 'POST / customers' create user

    When I create user <username>
    Then Verify user created

    Examples: Create User List

      | username  |
      | dishant   |
      | test_user |

  @create_user_api_inline_data_param
  Scenario: Verify 'POST / customers' create user inline data param

    When I create user ysmith
    Then Verify user created by inline data

  @create_user_step_data_param
  Scenario: Verify 'POST / customers' create user step data param

    When I create user
      | dishant  |
    Then Verify user created by step data
