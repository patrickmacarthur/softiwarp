#!/bin/bash

cp -r /var/tmp/softiwarp /var/tmp/build

kdir=/lib/modules/4.4.0-21-generic/build
make -C /var/tmp/build/kernel LINUX_SRC_PATH=${kdir} modules && \
    make -C /var/tmp/build/kernel LINUX_SRC_PATH=${kdir} clean
