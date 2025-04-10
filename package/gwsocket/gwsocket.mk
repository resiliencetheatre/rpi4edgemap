################################################################################
#
# GWSOCKET
#
################################################################################

GWSOCKET_VERSION = c17e13741ad2665ff463f94bfe7e425e5e97cf72
GWSOCKET_SITE = $(call github,allinurl,gwsocket,$(GWSOCKET_VERSION))
GWSOCKET_AUTORECONF = YES
GWSOCKET_LICENSE = GPL-2.0
GWSOCKET_LICENSE_FILES = COPYING
GWSOCKET_CONF_OPTS= --with-openssl

$(eval $(autotools-package))
