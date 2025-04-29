################################################################################
#
# thelounge
#
# NOTE: This needs yarn to be present at build host. Install it first.
#
################################################################################

THELOUNGE_VERSION = v4.4.3 
THELOUNGE_SITE =  $(call github,thelounge,thelounge,$(THELOUNGE_VERSION))

THELOUNGE_DEPENDENCIES = nodejs

THELOUNGE_MAKE_ENV = \
    $(TARGET_MAKE_ENV) \
    npm_config_arch=arm64 \
    npm_config_platform=linux \
    npm_config_build_from_source=true \
    npm_config_force_process_config=true \
    npm_config_update_binary=false \
    npm_config_fallback_to_build=false \
    CC="$(TARGET_CC)" \
    CXX="$(TARGET_CXX)" \
    AR="$(TARGET_AR)" \
    LD="$(TARGET_LD)" \
    STRIP="$(TARGET_STRIP)"
    
define THELOUNGE_CONFIGURE_CMDS
    # No configure step needed
endef

define THELOUNGE_BUILD_CMDS
    cd $(@D) && $(THELOUNGE_MAKE_ENV) yarn install --frozen-lockfile 
    cd $(@D) && NODE_ENV=production $(THELOUNGE_MAKE_ENV) yarn build
endef


define THELOUNGE_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/opt/thelounge
    mkdir -p $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/client $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/dist $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/index.js $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/LICENSE $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/node_modules $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/package.json $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/public $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/defaults $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/README.md $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
    cp -r $(@D)/.thelounge_home $(TARGET_DIR)/usr/lib/thelounge/node_modules/thelounge/
endef


$(eval $(generic-package))
