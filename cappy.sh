#!/bin/sh

echo "copying config for CAPPY"
cp arch/arm/configs/aries_captivate_defconfig .config

echo "building kernel"
make -j8

echo "creating boot.img"
../../../device/samsung/common/aries/mkshbootimg.py release/boot.img arch/arm/boot/zImage ../../../out/target/product/captivate/ramdisk.cpio.gz ../../../out/target/product/captivate/recovery.cpio.gz

echo "launching packaging script"
./release/doit_cappy.sh
