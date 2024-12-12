#
# kamailio sip server
#
KAMAILIO_VERSION = 8e398b8675079e1baac7c7575e70283175cdebe2
KAMAILIO_SITE = https://github.com/kamailio/kamailio.git
KAMAILIO_SITE_METHOD = git
KAMAILIO_DEPENDENCIES += mariadb sqlite
KAMAILIO_INSTALL_STAGING = YES
KAMAILIO_AUTORECONF = YES
KAMAILIO_CONF_OPTS = -DINCLUDE_MODULES="db_mysql db_sqlite"

$(eval $(cmake-package))
