#!/bin/bash

cp -r /var/tmp/softiwarp /var/tmp/build

for abi in 123 229 327 514; do
    kdir=/usr/src/kernels/3.10.0-${abi}.el7.x86_64
    make -C /var/tmp/build/kernel LINUX_SRC_PATH=${kdir} modules && \
        make -C /var/tmp/build/kernel LINUX_SRC_PATH=${kdir} clean
done
