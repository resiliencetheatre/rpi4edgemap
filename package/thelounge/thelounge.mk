################################################################################
#
# thelounge
#
# NOTE: This needs yarn to be present at build host. Install it first.
#
################################################################################
# #f97c4df2a28abf06a77e98b1ab16345300b212e7 
# ERROR: architecture for "/usr/lib/thelounge/node_modules/sqlite3/build/Release/node_sqlite3.node" is "Advanced Micro Devices X86-64", should be "AArch64"

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
    mkdir -p $(TARGET_DIR)/usr/lib/thelounge/node_modules/
    cp -r $(@D)/node_modules/* $(TARGET_DIR)/usr/lib/thelounge/node_modules/
endef


$(eval $(generic-package))
