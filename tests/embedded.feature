@verify
Feature: Embedded Cartridge Verification Tests

  Scenario: MySQL Embedded Usage
    Given the libra client tools
    And an accepted node
    When 1 php-5.3 applications are created
    Then the applications should be accessible
    Given an existing php-5.3 application without an embedded cartridge
    When the embedded mysql-5.1 cartridge is added
    Then the application should be accessible
    When the application uses mysql
    Then the application should be accessible
    And the mysql response is successful
    When the embedded cartridge is removed
    Then the application should be accessible
    When the application is destroyed
    Then the application should not be accessible    
    
  Scenario: Jenkins Client Usage
    Given the libra client tools
    And an accepted node
    When 1 jenkins-1.4 applications are created
    Then the applications should be accessible
    Given an existing jenkins-1.4 application without an embedded cartridge
    When the embedded jenkins-client-1.4 cartridge is added
    Then the application should be accessible
    When the embedded cartridge is removed
    Then the application should be accessible
    When the application is destroyed
    Then the application should not be accessible
    
