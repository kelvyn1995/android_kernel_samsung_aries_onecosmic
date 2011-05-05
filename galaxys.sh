#!/bin/sh

echo "copying config for SGS"
cp arch/arm/configs/aries_galaxys_defconfig .config

echo "building kernel"
make -j8

echo "creating boot.img"
../../../device/samsung/common/aries/mkshbootimg.py release/boot.img arch/arm/boot/zImage ../../../out/target/product/galaxys/ramdisk.cpio.gz ../../../out/target/product/galaxys/recovery.cpio.gz

echo "launching packaging script"
./release/doit.sh
