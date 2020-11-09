# -*- coding: utf-8 -*
@api @product_api
Feature: Product API Smoke

  @product_api_1
  Scenario: Verify 'Get all Products' returns the expected number of products

    Given I get number of available products from db
    When I get number of available products from API
    Then the total number of products in API should be same as in DB

  @product_api_2
  Scenario Outline: Verify 'Products/ID' returns a product with given ID

    Given I get <qty> random product from database
    Then  I verify products api returns correct product by id

    Examples: quantity of products
      | qty |
      | 5   |
      | 6   |
      | 4   |

  @product_api_3
  Scenario Outline: Verify Product Price of Random products get updated

    Given I update regular price of random products to <new_price>
    Then verify price updated

    Examples: Updated price of the Product
      | new_price |
      | 200       |
      | 100       |
      | 250       |

