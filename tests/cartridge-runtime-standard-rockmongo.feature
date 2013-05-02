@runtime
@runtime_extended2
Feature: rockmongo Embedded Cartridge

  Scenario Outline: Add remove rockmongo to one application
    Given a new <app_type> type application
    
    When I embed a mongodb-2.2 cartridge into the application
    And I embed a rockmongo-1.1 cartridge into the application
    Then the http proxy /rockmongo will exist
    And 4 processes named httpd will be running
    And the embedded rockmongo-1.1 cartridge directory will exist
    And the embedded rockmongo-1.1 cartridge log files will exist
    And the embedded rockmongo-1.1 cartridge control script will not exist

    When I stop the rockmongo-1.1 cartridge
    Then 2 processes named httpd will be running
    And the web console for the rockmongo-1.1 cartridge is not accessible

    When I start the rockmongo-1.1 cartridge
    Then 4 processes named httpd will be running
    And the web console for the rockmongo-1.1 cartridge is accessible
    
    When I restart the rockmongo-1.1 cartridge
    Then 4 processes named httpd will be running
    And the web console for the rockmongo-1.1 cartridge is accessible

    When I destroy the application
    Then 0 processes named httpd will be running
    And the http proxy /rockmongo will not exist
    And the embedded rockmongo-1.1 cartridge directory will not exist
    And the embedded rockmongo-1.1 cartridge log files will not exist
    And the embedded rockmongo-1.1 cartridge control script will not exist

  Scenarios:

    | app_type |
    | php-5.3  |