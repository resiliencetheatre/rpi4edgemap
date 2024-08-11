################################################################################
#
# python-rns
#
# https://files.pythonhosted.org/packages/a4/13/e1f0a10c961167d6a8ea5c9bb01be3199901be9334090a00f8b55a107d36/rns-0.7.5.tar.gz
################################################################################

PYTHON_RNS_VERSION = 0.7.5
PYTHON_RNS_SOURCE = rns-$(PYTHON_RNS_VERSION).tar.gz
PYTHON_RNS_SITE = https://files.pythonhosted.org/packages/a4/13/e1f0a10c961167d6a8ea5c9bb01be3199901be9334090a00f8b55a107d36
PYTHON_RNS_LICENSE = MIT
PYTHON_RNS_LICENSE_FILES = LICENSE-PSF LICENSE
PYTHON_RNS_SETUP_TYPE = setuptools
# This is a runtime dependency, but we don't have the concept of
# runtime dependencies for host packages.

$(eval $(python-package))