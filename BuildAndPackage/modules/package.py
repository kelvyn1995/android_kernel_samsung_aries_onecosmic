#!/usr/bin/env python3
#@package.py
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

"""Module that packages the kernel

This module includes:
 o make_boot_img(bootDisk, zImage, recovery = None):
    Makes a boot image from a zImage
    Returns a file-like object with boot.img written
    + bootDisk (string -> file): RAM Disk that phone boots from
    + zImage (string -> file): Built kernel
    % recovery (string -> file): RAM Disk that holds recovery mode

 o make_script(script, template):
    Edits a premade template to create the updater-script
    Returns None
    + script (string -> file): Location including script to output to
    + template (string -> file): Location including template to read from

 o make_zip(name, tree)
    Makes a non-compressed zipfile from a tree
    Returns None
    + name (string -> file): location including name to output to
    + tree (string -> directory): location to zip

 o prep_compilation(bootImgObj, destination, modules)
    Copies files to the zip directory
    Returns None
    + bootImgObj (object -> boot.img): File-like object with bootImg written
    + destinations (tuple->(string->folder, string->file)): Destination folder of the modules, destination file of the boot.img
    + modules(list -> [string -> module1, ...]): Compiled modules
"""

from error import FileAccessError

def make_boot_img(bootDisk, zImage, recovery = None):
    offsetTbl = '\n\nBOOT_IMAGE_OFFSETS\n'

    #Copy kernel into bootIMG
    try:
        with open(zImage, 'rb') as kernel:
            bootImg = kernel.read()

        #Change current location and record old one
        tableLoc = (len(bootImg) + 510) & -512
        bootImg += bytes('\x00' * (tableLoc - len(bootImg) + 512), 'utf-8')
    except IOError: raise FileAccessError(zImage)

    #Write the boot ramdisk to bootIMG 
    try:
        with open(bootDisk, 'rb') as ramDisk:
            bOffset = len(bootImg) - 1
            bootImg += ramDisk.read()
            offsetTbl += 'boot_offset={0};boot_len={1};'.format(1 + int(bOffset / 512), 1 + int((ramDisk.tell() + 1) / 512))
    except IOError: raise FileAccessError(bootDisk)

    #Write the recovery to bootIMG and add it's entry to the 
    if recovery:
        try:
            with open(recovery, 'rb') as ramDisk:
                bOffset = len(bootImg) - 1
                bootImg += bytes('\x00' * (((len(bootImg) + 510) & -512) - len(bootImg)), 'utf-8') + ramDisk.read()
                offsetTbl += 'recovery_offset={0};recovery_len={1};\n\n'.format(int(1 + bOffset / 512), int(1 + (ramDisk.tell() + 1) / 512))
        except IOError: raise FileAccessError(recovery)

    bootImg = bootImg[:tableLoc] + bytes(offsetTbl, 'utf-8') + bootImg[tableLoc + len(offsetTbl):] 

    return bootImg

def make_script(device, script, template, version):
    from datetime import datetime
    from os import getlogin

    #Open the script and template up
    try:
        with open(script, 'w+') as scriptUpdtr:
            try:
                with open(template, 'r') as template:
                    #Re-write the updater script with information baked in
                    scriptUpdtr.write(template.read().format(device, getlogin(), str(datetime.utcnow()) + ' UTC', version))
            except IOError: FileAccessError(template)
    except IOError: FileAccessError(script)

def make_zip(name, tree):
    from os import walk, sep
    from zipfile import ZipFile, ZIP_STORED

    #Try opening a zip file and copying the tree via recursion into it
    try:
        with ZipFile(name, 'w', ZIP_STORED) as fuguZip:
            for root, folders, files in walk(tree):
                zipRoot = root[len(tree) + 1:]
                #zipRoot = root[len(tree + curdir + sep) - 1:]

                if files:
                    for fileName in files:
                        fuguZip.write(root + sep + fileName, zipRoot + sep + fileName)
                else: continue              
    except IOError: raise FileAccessError(name)

def prep_compilation(bootImgObj, destinations, modules):
    from os import mkdir
    from shutil import copy

    #Copy modules
    for module in modules: copy(module, destinations[0])

    #Write the boot.img to the tree, if it fails, cry!
    try:
        with open(destinations[1], 'w+b') as bootImgFile:
            bootImgFile.write(bootImgObj)
    except IOError: FileAccessError(destinations[1])