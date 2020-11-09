# -*- coding: utf-8 -*-
@api @user_api_delete
Feature: UserDelete API Smoke

  @delete_user_api
  Scenario Outline: Verify Delete User

    When I Delete user <username>
    Then Verify user deleted <username>

    Examples: Username to Delete
      | username |
      | ysmith   |
      | mark32   |

  @create_user_api_inline_data_param
  Scenario: Verify Delete User by inline data param

    When I Delete user ysmith
    Then Verify user deleted ysmith

  @create_user_step_data_param
  Scenario: Verify Delete User by step data param

    When I Delete user
      | username |
      | mark32   |
    Then Verify user deleted
      | username |
      | mark32   |
