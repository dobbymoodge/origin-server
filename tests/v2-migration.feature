@runtime_migration
Feature: V2 Migrations for V1 apps
  Scenario: PHP app migration
    Given a new client created php-5.3 application
    And the application has a USER_VARS env file
    And the application has a TYPELESS_TRANSLATED_VARS env file
    And the application has a TRANSLATE_GEAR_VARS env file
    Then the application should be accessible

    When the application is migrated to the v2 cartridge system
    Then the environment variables will be migrated to raw values
    And the application will be marked as a v2 app
    And the application should be accessible
    And the USER_VARS file will not exist
    And the TRANSLATE_GEAR_VARS file will not exist
    And the TYPELESS_TRANSLATED_VARS variables will be discrete variables

  Scenario: Stopped PHP app migration
    Given a new client created php-5.3 application
    And the application is stopped

    When the application is migrated to the v2 cartridge system
    Then the environment variables will be migrated to raw values
    And the application will be marked as a v2 app
    And the application should not be accessible
