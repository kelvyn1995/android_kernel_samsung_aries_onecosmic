#!/bin/sh

echo "copying config for SGS"
cp arch/arm/configs/aries_vibrant_defconfig .config

echo "building kernel"
make -j8

echo "creating boot.img"
../../../device/samsung/common/aries/mkshbootimg.py release/boot.img arch/arm/boot/zImage ../../../out/target/product/vibrant/ramdisk.cpio.gz ../../../out/target/product/vibrant/recovery.cpio.gz

echo "launching packaging script"
./release/doit_vibrant.sh
