#!/usr/bin/env python3
#@get_configs.py
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

from error import FileAccessError
from os import sep
from sys import path

class GetConfigs:
    """Class that grabs the configuration from files

This class includes:
    o device_settings():
        Makes a table of devices from devices.cfg
        Returns the table of devices

    o user_settings():
        Makes GetConfigs into a holder for variables declared in userSettings.cfg
        Returns None
    """

    def __init__(self):
        self.mainPath = path[0]
        self.resources = '{0}{1}BuildAndPackage{1}resources{1}'.format(self.mainPath, sep)

    def device_settings(self):
        try: 
            with open(self.resources + 'devices.cfg', 'r') as devices:
                index = 0
                tabDevices = list()

                while True:
                    #Get the device name, if possible
                    nameLine = devices.readline()
                    if not nameLine: break

                    #Find each name and add it, if it's a bad line skip it
                    start = nameLine.find('e = ') + 4
                    if start < 4: continue
                    else: nameDev = nameLine[start: nameLine.find('\n')]

                    #Get device defconfig
                    defLine = devices.readline()
                    defDev = (defLine[defLine.find('g = ') + 4: defLine.find('\n')])

                    #Increment index and add info to tabDevices
                    index += 1
                    tabDevices += nameDev, defDev,
                return tabDevices
        except IOError: raise FileAccessError(self.resources + 'devices.cfg')

    def user_settings(self):
        try:
            with open(self.resources + 'userSettings.cfg', 'r') as userSettings:
                #Replace all placeholders except the one for git revision thing
                userConf = userSettings.read().format(sep, self.mainPath + sep, '{0}')

                #Lambda to get the variable
                get_var = lambda keyword: userConf[userConf.find(keyword) + len(keyword): userConf.find(keyword) + userConf[userConf.find(keyword):].find('\n')]

                #Set variables
                #Perhaps this can be made more high level later; for now we stick with what works
                self.cFlags = get_var('cflags = ').split('; ')
                self.clean = get_var('clean = ')
                self.cppFlags = get_var('cppflags = ').split('; ')
                self.initRAMDisk = get_var('initial-ramdisk = ')
                self.ldFlags = get_var('ldflags = ').split('; ')
                self.modules = get_var('modules = ').split('; ')
                self.recoRAMDisk = get_var('recovery-ramdisk = ')
                self.toolchain = get_var('toolchain = ')
                self.version = get_var('version = ')
                self.kernel = get_var('zImage = ')

                #Do any other work needed to the variables
                if len(self.clean) > 100: self.clean = False
                else: self.clean = True

        except IOError: raise FileAccessError(self.resources + 'userSettings.cfg')