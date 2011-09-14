#!/bin/sh

#echo "environment set-up"

#export ARCH=arm 
#export TOOLCHAIN=/opt/toolchains/arm-2009q3
#export TOOLPREFIX=arm-none-linux-gnueabi
##export PATH=$PATH:${TOOLCHAIN}/bin:/usr/java/jdk1.6.0_21/bin
#export CROSS_COMPILE=${TOOLCHAIN}/bin/${TOOLPREFIX}-
#export CC=${TOOLCHAIN}/bin/${TOOLPREFIX}-gcc
#export LD=${TOOLCHAIN}/bin/${TOOLPREFIX}-ld
#export AR=${TOOLCHAIN}/bin/${TOOLPREFIX}-ar
#export RANLIB=${TOOLCHAIN}/arm-eabi/bin/ranlib
#export PATH=$PATH:${TOOLCHAIN}/bin
#export PATH=$PATH:${TOOLCHAIN}/
#export PATH=$PATH:${TOOLCHAIN}/lib
##export CFLAGS="-mcpu=cortex-a8 -mfpu=neon -mfloat-abi=softfp -static -Os -fstack-protector -fstack-protector-all -fno-gcse -fprefetch-loop-arrays --param l2-cache-size=512 --param l1-cache-size=64 --param simultaneous-prefetches=6 #--param prefetch-latency=400 --param l1-cache-line-size=64 -std=c99"
export CFLAGS="-static -O2 -std=c99 -mtune=cortex-a8 --param l2-cache-size=256 --param l1-cache-size=16 --param simultaneous-prefetches=8 --param prefetch-latency=200 --param l1-cache-line-size=32 -fsched-spec-load-dangerous -fpredictive-commoning -fira-coalesce -funswitch-loops -ftree-loop-im -fipa-cp-clone"
export LDFLAGS="-static -O2"
export CPPFLAGS="-static -O2"

# -std=c99
# -fstack-protector -fstack-protector-all

#echo "ARM environment set"

echo "proceeding to kernel-compilation"

echo "copying config for SGS"
cp arch/arm/configs/aries_galaxysmtd_defconfig .config

echo "building kernel"
make -j8

echo "creating boot.img"
../../../device/samsung/aries-common/mkshbootimg.py release/boot.img arch/arm/boot/zImage ../../../out/target/product/galaxysmtd/ramdisk.img ../../../out/target/product/galaxysmtd/ramdisk-recovery.img

echo "launching packaging script"
./release/doit.sh
