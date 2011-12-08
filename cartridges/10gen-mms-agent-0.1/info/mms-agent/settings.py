"""
(C) Copyright 2011, 10gen

Unless instructed by 10gen, do not modify default settings.

When upgrading your agent, you must also upgrade your settings.py file.
"""

#
# Seconds between Mongo status checks
#
collection_interval = 56

#
# Seconds between cloud configuration checks
#
conf_interval = 120

#
# The mms server
#
mms_server = "https://mms.10gen.com"

#
# The mms ping url
#
ping_url = mms_server + "/ping/v1/%s"

#
# The mms config url
#
config_url = mms_server + "/conf/v2/%(key)s?am=true&ah=%(hostname)s&sk=%(sessionKey)s&av=%(agentVersion)s"

#
# The mms agent version url
#
version_url = mms_server + "/agent/v1/version/%(key)s"

#
# The mms agent upgrade url
#
upgrade_url = mms_server + "/agent/v1/upgrade/%(key)s"

#
# The mms agent log path.
#
logging_url = mms_server + "/agentlog/v1/catch/%(key)s"

#
# Enter your API key  - See: http://mms.10gen.com/settings
#
mms_key = "015b7af6be43e64a2706178183bb21c2"

secret_key = "46ac0cec6caea162be6be8f0b04041e6"

#
# Enabled by default
#
autoUpdateEnabled = True

#
# Some config db collection properties
#
configCollectionsEnabled = True
configDatabasesEnabled = True

settingsAgentVersion = "1.3.7"

# Misc
socket_timeout = 30

