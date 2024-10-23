################################################################################
#
# python-yarl
#
################################################################################

PYTHON_YARL_VERSION = 1.15.5
PYTHON_YARL_SOURCE = yarl-$(PYTHON_YARL_VERSION).tar.gz
PYTHON_YARL_SITE = https://files.pythonhosted.org/packages/3e/83/529d9cb66a6b3ba120c4a52bec8299f495f9446b749cb1110c89ffb46704
PYTHON_YARL_LICENSE = Apache-2.0
PYTHON_YARL_LICENSE_FILES = LICENSE
PYTHON_YARL_SETUP_TYPE = setuptools

$(eval $(python-package))
