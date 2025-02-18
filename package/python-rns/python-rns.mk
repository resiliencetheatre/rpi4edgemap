################################################################################
#
# python-rns
#
################################################################################

PYTHON_RNS_VERSION = 0.9.2
PYTHON_RNS_SITE = $(call github,markqvist,Reticulum,$(PYTHON_RNS_VERSION))
PYTHON_RNS_LICENSE = MIT
PYTHON_RNS_LICENSE_FILES = LICENSE-PSF LICENSE
PYTHON_RNS_SETUP_TYPE = setuptools

$(eval $(python-package))
