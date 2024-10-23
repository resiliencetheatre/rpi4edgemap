################################################################################
#
# python-propcache
#
# https://pypi.org/project/propcache/
#
#
################################################################################

PYTHON_PROPCACHE_VERSION = 0.2.0
PYTHON_PROPCACHE_SOURCE = propcache-$(PYTHON_PROPCACHE_VERSION).tar.gz
PYTHON_PROPCACHE_SITE = https://files.pythonhosted.org/packages/a9/4d/5e5a60b78dbc1d464f8a7bbaeb30957257afdc8512cbb9dfd5659304f5cd
PYTHON_PROPCACHE_LICENSE = MIT
PYTHON_PROPCACHE_LICENSE_FILES = LICENSE-PSF LICENSE
PYTHON_PROPCACHE_SETUP_TYPE = setuptools
# This is a runtime dependency, but we don't have the concept of
# runtime dependencies for host packages.

$(eval $(python-package))
