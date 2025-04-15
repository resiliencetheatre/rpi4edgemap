IRCPIPE_VERSION = 4e2d42b00d60fab6a8efdcd4083d092b7a4e670c
IRCPIPE_SITE = https://codeberg.org/resiliencetheatre/ircpipe.git
IRCPIPE_SITE_METHOD = git
IRCPIPE_PREFIX = $(TARGET_DIR)/usr
IRCPIPE_LICENSE = gplv3

define IRCPIPE_BUILD_CMDS
     $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D)
endef

define IRCPIPE_INSTALL_TARGET_CMDS
        (cd $(@D); cp ircpipe $(IRCPIPE_PREFIX)/bin)
endef

define IRCPIPE_CLEAN_CMDS
        $(MAKE) $(IRCPIPE_MAKE_OPTS) -C $(@D) clean
endef

$(eval $(generic-package))
