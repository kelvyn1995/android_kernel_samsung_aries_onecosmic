#!/bin/bash

export KBUILD_BUILD_VERSION="Neo-11-mod"

echo "copying config for Captivate"
cp arch/arm/configs/aries_captivatemtd_defconfig .config

echo "building kernel"
cd drivers/misc/samsung_modemctl/modemctl
make
cd ..
make
cd ../../..
make -j`grep 'processor' /proc/cpuinfo | wc -l`

