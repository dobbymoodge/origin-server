#
# Global definitions
#
AMI = "ami-7dea2614"
TYPE = "m1.large"
KEY_PAIR = "libra"
ZONE = 'us-east-1d'
DEVENV_REGEX = /devenv\_/
DEVENV_STAGE_REGEX = /devenv-stage\_/
DEVENV_CLEAN_REGEX = /devenv-clean\_/
TERMINATE_REGEX = /terminate/
VERIFIED_TAG = "qe-ready"
RSA = File.expand_path("~/.ssh/libra.pem")
SSH = "ssh 2> /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o PasswordAuthentication=no -i " + RSA
SCP = "scp 2> /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o PasswordAuthentication=no -i " + RSA

$amz_options = {:key_name => KEY_PAIR, :instance_type => TYPE, :availability_zone => ZONE}
