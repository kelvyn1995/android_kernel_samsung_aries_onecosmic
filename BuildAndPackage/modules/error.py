#!/usr/bin/env python3
#@error.py
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

#File access issues
class FileAccessError:
    def __init__(self, fileName):
        print('Locked or non-existant file: ' + fileName)
        exit(1)

#Build errors
class BuildError:
    def __init__(self):
        print('Build Failed!')
        exit(1)