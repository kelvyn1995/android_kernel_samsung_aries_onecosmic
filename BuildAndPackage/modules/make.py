#!/usr/bin/env python3
#@make.py
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

"""Module that makes the kernel

This module includes:
  o build(toolchain, log):
     Builds the kernel
     Returns None
     log (string -> file): Log file to write to
     toolchain (string -> directory with prefix): Location of the toolchain to use

  o configure(defconfig, clean = False):
     Imports the defconfig and cleans if wanted
     Returns None
     defconfig (string -> device defconfig): Device defconfig
     clean (bool): Clean before make?
     dMain (string -> main directory): used to determine whether we copy defconf
     manually, or we use make; also tells us the main directory.

  o revision():
     Gets Git revision (REQUIRES A TAG!)
     Returns revision number
"""

from subprocess import Popen, PIPE

def build(log, toolchain):
    from error import BuildError
    from multiprocessing import cpu_count

    with open(log, 'w+') as buildLog:
        buildLog.write('----------BUILD PROCESS START---------\n')
        buildLog.write(str(Popen(['make', 'ARCH=arm', '-j' + str(cpu_count() + 1), 'CCACHE=1', 'CROSS_COMPILE={0}'.format(toolchain)], stdout = PIPE).communicate()[0], 'utf-8'))
        buildLog.write('-----------BUILD PROCESS END-----------\n')

        #Error checking code
        buildLog.seek(0, 0)
        if buildLog.read().find('zImage is ready') == -1: raise BuildError()

def configure(defconfig, clean = False):
    from os import sep
    from shutil import copyfile

    if clean: Popen(['make', 'clean']).wait()
    Popen(['make', defconfig, 'ARCH=arm']).wait()

def revision():
    revision = str(Popen(['git', 'describe'], stdout = PIPE).communicate()[0], 'utf-8')
    return revision[6: revision[6:].find('-') + 6]