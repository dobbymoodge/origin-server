@internals
Feature: PostgreSQL Application Sub-Cartridge
  
  Scenario Outline: Create one application with a PostgreSQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    When I configure a postgresql database
    Then the postgresql directory will exist
    And the postgresql configuration file will exist
    And the postgresql database will exist
    And the postgresql control script will exist
    And the postgresql daemon will be running
    And the admin user will have access

  Scenarios: Create Application With Database Scenarios
    |type|
    |php|
    

  Scenario Outline: Delete one PostgreSQL Database from an Application
    Given an accepted node
    And a new guest account
    And a new <type> application
    And a new postgresql database
    When I deconfigure the postgresql database
    Then the postgresql daemon will not be running
    And the postgresql database will not exist
    And the postgresql control script will not exist
    And the postgresql configuration file will not exist
    And the postgresql directory will not exist

  Scenarios: Delete one PostgreSQL database Scenarios
    |type|
    |php|

    
  Scenario Outline: Start a PostgreSQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    And a new postgresql database
    And the postgresql daemon is stopped
    When I start the postgresql database
    Then the postgresql daemon will be running

  Scenarios: Start a PostgreSQL database scenarios
    |type|
    |php|
    

  Scenario Outline: Stop a PostgreSQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    And a new postgresql database
    And the postgresql daemon is running
    When I stop the postgresql database
    Then the postgresql daemon will not be running



  Scenarios: Stop a PostgreSQL database scenarios
    |type|
    |php|

  Scenario Outline: Restart a PostgreSQL database
    Given an accepted node
    And a new guest account
    And a new <type> application
    And a new postgresql database
    And the postgresql daemon is running
    When I restart the postgresql database
    Then the postgresql daemon will be running
    And the postgresql daemon pid will be different

  Scenarios: Restart a PostgreSQL database scenarios
     |type|
     |php|

