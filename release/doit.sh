#!/bin/sh

[[ -d release ]] || {
	echo "must be in kernel root dir"
	exit 1;
}


TYPE=$1
[[ "$TYPE" == '' ]] && TYPE=SGS

REL=CM7_${TYPE}_platypus-kernel_$(date +%Y%m%d_%H)_update.zip

cp ./arch/arm/boot/zImage release/ || exit 1
find . -name "*.ko" -exec cp {} release/system/modules/ \; 2>/dev/null || exit 1

cd release && {
	zip -q -r ${REL} system zImage META-INF || exit 1
	sha256sum ${REL} > ${REL}.sha256sum
	rm -rf ${TYPE} || exit 1
	mkdir -p ${TYPE} || exit 1
	mv ${REL}* ${TYPE} || exit 1
} || exit 1

rm system/modules/*
echo ${REL}
exit 0
