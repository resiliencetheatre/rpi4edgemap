To use these updated .mk files, delete hash files and copy these
over to your buildroot/package/ directory.

# python-cython
rm  [buildroot_directory]/package/python-cython/python-cython.hash
cp python-cython.mk [buildroot_directory]/package/python-cython

# python-yarl
rm [buildroot_directory]/package/python-yarl/python-yarl.hash
cp python-yarl.mk [buildroot_directory]/package/python-yarl
