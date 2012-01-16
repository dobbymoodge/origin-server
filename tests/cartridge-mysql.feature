@internals
Feature: MySQL Application Sub-Cartridge
  
  Scenario Outline: Create Delete one application with a MySQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    When I configure a mysql database
    Then the mysql directory will exist
    And the mysql configuration file will exist
    And the mysql database will exist
    And the mysql control script will exist
    And the mysql daemon will be running
    And the admin user will have access
    When I deconfigure the mysql database
    Then the mysql daemon will not be running
    And the mysql database will not exist
    And the mysql control script will not exist
    And the mysql configuration file will not exist
    And the mysql directory will not exist

  Scenarios: Create Delete Application With Database Scenarios
    |type|
    |php|
    
  Scenario Outline: Start Restart a MySQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    And a new mysql database
    And the mysql daemon is stopped
    When I start the mysql database
    Then the mysql daemon will be running
    When I restart the mysql database
    Then the mysql daemon will be running
    And the mysql daemon pid will be different
    And I deconfigure the mysql database

  Scenarios: Start Restart a MySQL database scenarios
    |type|
    |php|
    

  Scenario Outline: Stop a MySQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    And a new mysql database
    And the mysql daemon is running
    When I stop the mysql database
    Then the mysql daemon will not be running
    And I deconfigure the mysql database

  Scenarios: Stop a MySQL database scenarios
    |type|
    |php|

