@internals
Feature: Raw Application

  # runcon -u ?? -r system_r -t libra_initrc_t

  Scenario: Create one Raw Application
    Given an accepted node
    And a new guest account
    And the guest account has no application installed
    When I configure a raw application
    Then a raw application http proxy file will exist
    And a raw application git repo will exist
    And a raw application source tree will exist

  Scenario: Delete one Raw Application
    Given an accepted node
    And a new guest account
    And a new raw application
    When I deconfigure the raw application
    And a raw application git repo will not exist
    And a raw application source tree will not exist
