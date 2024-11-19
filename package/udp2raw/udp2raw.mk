UDP2RAW_VERSION = fe3725954fe173789e043b9d1d600afc6754d1a6
UDP2RAW_SITE = https://github.com/resiliencetheatre/udp2raw.git
UDP2RAW_SITE_METHOD = git
UDP2RAW_PREFIX = $(TARGET_DIR)/usr

define UDP2RAW_BUILD_CMDS
     $(MAKE) CXX=$(TARGET_CXX)  -C $(@D)
endef

define UDP2RAW_INSTALL_TARGET_CMDS
        (cd $(@D); cp udp2raw $(UDP2RAW_PREFIX)/bin)
endef

define UDP2RAW_CLEAN_CMDS
        $(MAKE) $(UDP2RAW_MAKE_OPTS) -C $(@D) clean
endef

$(eval $(generic-package))
