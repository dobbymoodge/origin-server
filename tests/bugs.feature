@verify
Feature: cucumber tests for reported bugs

  #bug 701676, already has cucumber test, see userstory_steps:#US280 - TC19 

  Scenario: (libra-qe) bug 693951: rhc-create-domain suggests --alter can be used to rename domain
    Given an end user
    Then he could create a namespace and app
    When he alter the namespace
    Then the new namespace is enabled

#  Scenario: (libra-qe) bug 701159: posting data with http instead of https
#    Given the following website links
#      |         uri          |  protocol  |
#      | /                    |    http    |
#      | /app                 |    http    |
#      | /app/getting_started |    http    |
#      | /app/user/new        |    http    |
#    Then come into an error when they are accessed

  Scenario: (libra-qe) bug 700941: Express client installation has empty README files under AppName/misc and AppName/libs
    Given the libra client tools
    And create a new php-5.3.2 app 'phpbug'
    Then no README under misc and libs

  Scenario: (libra-qe) bug 699887: PHP $_SERVER["HTTP_HOST"] returns wrong value
    Given the libra client tools
    And create a new php-5.3.2 app 'phphost'
    Then can get host name using php script

  Scenario: (libra-qe) Bug 695586 - man page of express.conf is empty
    Given the libra client tools
    And the manpage of express.conf
    Then the manpage of express.conf should not be empty



