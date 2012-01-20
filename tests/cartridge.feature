@verify
Feature: Cartridge Verification Tests
  Scenario Outline: Application Creation
    Given the libra client tools
    And an accepted node
    When <app_count> <type> applications are created
    Then the applications should be accessible

  Scenarios: Application Creation Scenarios
    | app_count |     type     |
    |     1     |  php-5.3     |
    |     1     |  wsgi-3.2    |
    |     1     |  perl-5.10   |
    |     1     |  ruby-1.8    |
    |     1     |  jbossas-7.0 |
    |     1     |  jenkins-1.4 |
    |     1     |  raw-0.1     |

  Scenario Outline: Application Modification
    Given an existing <type> application
    When the application is changed
    Then it should be updated successfully
    And the application should be accessible

  Scenarios: Application Modification Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |

  Scenario Outline: Application Stopping
    Given an existing <type> application
    When the application is stopped
    Then the application should not be accessible

  Scenarios: Application Stopping Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |

  Scenario Outline: Application Starting
    Given an existing <type> application
    When the application is started
    Then the application should be accessible

  Scenarios: Application Starting Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |

  Scenario Outline: Server Alias
    Given an existing <type> application
    When the application is aliased
    Then the application should respond to the alias

  Scenarios: Server Alias Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |

  Scenario Outline: Application Restarting
    Given an existing <type> application
    When the application is restarted
    Then the application should be accessible

  Scenarios: Application Restart Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |

  Scenario Outline: Application Restarting From Stop
    Given an existing <type> application
    When the application is stopped
    And the application is restarted
    Then the application should be accessible

  Scenarios: Application Restarting From Stop Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jenkins-1.4 |
    
  Scenario Outline: Application Change Namespace
    Given an existing <type> application
    When the application namespace is updated
    Then the application should be accessible

  Scenarios: Application Change Namespace Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |
    
  Scenario Outline: Application Snapshot
    Given an existing <type> application
    When I snapshot the application
    Then the application should be accessible
    When I restore the application
    Then the application should be accessible

  Scenarios: Application Snapshot Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |
    |   raw-0.1     |

  Scenario Outline: Application Tidy
    Given an existing <type> application
    When I tidy the application
    Then the application should be accessible

  Scenarios: Application Tidy Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |
    |   raw-0.1     |

  Scenario Outline: Application Destroying
    Given an existing <type> application
    When the application is destroyed
    Then the application should not be accessible

  Scenarios: Application Destroying Scenarios
    |      type     |
    |   php-5.3     |
    |   wsgi-3.2    |
    |   perl-5.10   |
    |   ruby-1.8    |
    |   jbossas-7.0 |
    |   jenkins-1.4 |
