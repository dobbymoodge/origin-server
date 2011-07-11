@regression
Feature: Cucumber tests for reported bugs

  Scenario: (libra-qe) Bug 693951 - Command 'rhc-create-domain --alter' can not be used to rename domain
    Given an end user
    And he can create a namespace and app
    When he alters the namespace
    Then the new namespace is enabled

  Scenario: (libra-qe) Bug 699887 - PHP $_SERVER["HTTP_HOST"] returns wrong value
    Given the libra client tools
    When a new php-5.3 app 'phphost' is created
    Then the host name can be obtained using php script

  Scenario: (libra-qe) Bug 688045 - The arithmetics of git_repos facter is not reasonable.
    Given the libra client tools
    And an accepted node
    When check the number of the git files in libra dir
    And check the number of git repos by mc-facts
    Then the first number is twice the second one
    Given the following test data
      | processes | users | apps |   type   |
      |     2     |   2   |  1   | php-5.3  |
    When the applications are created
    Then they should all be accessible
    When check the number of the git files in libra dir
    And check the number of git repos by mc-facts
    Then the second one adds 2
    And the first number is twice the second one

  Scenario: (libra-qe) Bug 688820 - create more than one domain with same namespace
    Given the libra client tools
    And an accepted node
    When create two domains with same namespace
    Then this operation should fail

  Scenario: (libra-qe) Bug 688893 - Error happens when start wsgi app using rhc-ctl-app
    Given the libra client tools
    And an accepted node
    And the following test data
      | processes | users | apps |   type   |
      |     1     |   1   |  1   | wsgi-3.2 |
    When the applications are created
    Then they should all be accessible
    When the applications are stopped
    Then they should all be able to start
    And they should all be accessible

  Scenario: (libra-qe) Bug 693975 - rhc-ctl-app reload command will make app does not work any more
    Given the libra client tools
    And an accepted node
    And the following test data
      | processes | users | apps |   type   |
      |     1     |   1   |  1   | php-5.3  |
    When the applications are created
    Then they should all be accessible
    When the applications are reloaded
    Then they should all be accessible

  Scenario: (libra-qe) Bug 685078 - Error happens when check app status using rhc-ctl-app
    Given the libra client tools
    And an accepted node
    And the following test data
      | processes | users | apps |   type   |
      |     1     |   1   |  1   | php-5.3  |
    When the applications are created
    Then they should all be accessible
    When check status of the applications
    Then no errors should be thrown

  Scenario: (libra-qe) Bug 685118 - one user can create 11 apps when set "per_user_app_limit=10" (current limit=5)
    Given the libra controller configuration
    And the libra client tools
    And an accepted node
    When the libra controller configuration
    Then the number of apps per user is 5
    Given the following test data
      | processes | users | apps |   type   |
      |     5     |   1   |  5   | php-5.3  |
    When the applications are created
    Then no errors should be thrown
    When create more than 5 apps for the user
    Then this operation should fail
