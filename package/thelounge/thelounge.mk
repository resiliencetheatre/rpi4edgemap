################################################################################
#
# thelounge
#
# NOTE: This needs yarn to be present at build host. Install it first.
#
################################################################################

THELOUNGE_VERSION = f97c4df2a28abf06a77e98b1ab16345300b212e7 
THELOUNGE_SITE =  $(call github,thelounge,thelounge,$(THELOUNGE_VERSION))

THELOUNGE_DEPENDENCIES = nodejs


define THELOUNGE_CONFIGURE_CMDS
    # No configure step needed
endef

define THELOUNGE_BUILD_CMDS
	# --frozen-lockfile
    cd $(@D) && yarn install 
endef

define MYPACKAGE_INSTALL_TARGET_CMDS
    # Example: Copy built 'dist' directory into /var/www/mypackage on target
    # mkdir -p $(TARGET_DIR)/var/www/mypackage
    # cp -r $(@D)/dist/* $(TARGET_DIR)/var/www/mypackage/
endef


$(eval $(generic-package))
