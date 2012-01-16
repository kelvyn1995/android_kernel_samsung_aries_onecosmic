#!/usr/bin/env python3
#@BuildAndPackage.py
#
# Copyright 2011 Trae Santiago
# ================================================
#
# This file is part of BuildAndPackage
#
# BuildAndPackage is free software: you 
# can redistribute it and/or modify it under the 
# terms of the GNU General Public License as 
# published by the Free Software Foundation, 
# either version 3 of the License, or (at your 
# option) any later version.
# 
# BuildAndPackage is distributed in the
# hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License 
# for more details.
# 
# You should have received a copy of the GNU 
# General Public License along with BuildAndPackage. 
# If not, see: <http://www.gnu.org/licenses/>.
# (T.S / T.B / Trae32566 / Trae Santiago)

from os import sep
from sys import path

bapDir = '{0}{1}BuildAndPackage'.format(path[0], sep)

def main():
    #Add our module directory to the path and import modules
    path.append('{0}{1}modules{1}'.format(bapDir, sep))
    import get_configs

    #Set variables
    count = 0

    #Get config and devices
    config = get_configs.GetConfigs()
    config.user_settings()
    devices = config.device_settings()

    #Start working!
    #worker(config, 'SGH-i897_Captivate', 'aries_captivatemtd_defconfig', 4)
    for device in devices[::2]:
        worker(config, device, devices[1::2][count])

        count += 1


def worker(config, nameDev, defDev):
    from os import pardir, mkdir
    from os.path import isdir
    from shutil import copytree, rmtree
    import make, package

    config.version = config.version.format(make.revision())        
    dirDev = bapDir + sep + nameDev

    #Make the directory for the device and copy the zip into it (delete any existing ones)
    if isdir(dirDev): rmtree(dirDev)
    copytree('{0}{1}zip'.format(bapDir, sep), dirDev)
    mkdir('{0}{1}system{1}lib'.format(dirDev, sep))
    mkdir('{0}{1}system{1}lib{1}modules'.format(dirDev, sep))

    #Start configuring, build, get revision number
    make.configure(defDev, config.clean)
    make.build(bapDir + sep + nameDev + '.log', config.toolchain)

    #Start packaging
    package.make_script(nameDev, 
                        '{0}{1}META-INF{1}com{1}google{1}android{1}updater-script'.format(dirDev, sep),  '{0}{1}resources{1}updater-script.template'.format(bapDir, sep), 
                        config.version)
    package.prep_compilation(package.make_boot_img(config.initRAMDisk, config.kernel, config.recoRAMDisk), 
                             ('{0}{1}system{1}lib{1}modules{1}'.format(dirDev, sep), dirDev + sep + 'boot.img'),
                             config.modules)
    package.make_zip((dirDev + sep + pardir + sep + '[Kernel]-' + nameDev + '-' + config.version + '.zip'), dirDev)

    #Clean
    rmtree(dirDev)

main()