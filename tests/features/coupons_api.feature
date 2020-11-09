# -*- coding: utf-8 -*
@api @coupon
Feature:Create coupon

  Scenario Outline: Create Coupon with minimum parameters should create coupon

    Given I create a <discount_type> coupon with <amount>
    Then coupon should be created

    Examples:
      | discount_type | amount |
      | percent       | 20     |
      | fixed_cart    | 50     |