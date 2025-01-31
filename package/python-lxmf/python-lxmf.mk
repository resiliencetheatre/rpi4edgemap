################################################################################
#
# python-lxmf
#
################################################################################

PYTHON_LXMF_VERSION = 0.6.2
PYTHON_LXMF_SITE = $(call github,markqvist,LXMF,$(PYTHON_LXMF_VERSION))
PYTHON_LXMF_LICENSE = MIT
PYTHON_LXMF_LICENSE_FILES = LICENSE-PSF LICENSE
PYTHON_LXMF_SETUP_TYPE = setuptools
# This is a runtime dependency, but we don't have the concept of
# runtime dependencies for host packages.

$(eval $(python-package))
