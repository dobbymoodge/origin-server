@sprint1
Feature: Setup a new application

  Scenario:
    Given the libra client tools
    And 10 concurrent processes
    And 100 new users
    When 10 applications of type 'php-5.3.2' are created per user
    Then they should all be accessible
