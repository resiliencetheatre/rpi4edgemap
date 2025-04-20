################################################################################
#
# CryptPad
#
################################################################################

CRYPTPAD_VERSION = a24370f0f27ec81dec107d563e9573eb652e8a05 
CRYPTPAD_SITE =  $(call github,cryptpad,cryptpad,$(CRYPTPAD_VERSION))

CRYPTPAD_DEPENDENCIES = nodejs

CRYPTPAD_MAKE_ENV = \
    npm_config_arch=arm64 \
    npm_config_platform=linux \
    npm_config_build_from_source=true \
    npm_config_update_binary=false \
    npm_config_fallback_to_build=true

define CRYPTPAD_CONFIGURE_CMDS
    cd $(@D) && npm install --omit=dev
endef

define CRYPTPAD_BUILD_CMDS
    # Build server components (optional)
    cd $(@D) && npm run install:components
endef

define CRYPTPAD_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/opt/cryptpad
    cp -r $(@D)/* $(TARGET_DIR)/opt/cryptpad/
endef

$(eval $(generic-package))
