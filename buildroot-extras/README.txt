To use these updated .mk files, delete hash files and copy these
over to your buildroot/package/ directory. 

NOTE: Original buildroot/package directory contains buildroot provided
package files and rpi4edgemap/package contains packages added to edgemap
build. 

We need to update following buildroot provided packages to successful 
compile image. You can use following .mk files to upgrade these packages.


# espflash 3.2.0
rm [buildroot_directory]/package/espflash/espflash.hash
cp espflash.mk [buildroot_directory]/package/espflash/

# libcodec2 1.2.0
rm [buildroot_directory]/package/libcodec2/libcodec2.hash
cp libcodec2.mk [buildroot_directory]/package/libcodec2/libcodec2.hash
