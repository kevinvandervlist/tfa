# Settings class
# Copyright (C) 2012 Kevin van der Vlist, Rosco Voorrips
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Kevin van der Vlist - kevin@kevinvandervlist.nl
# Rosco Voorrips

""" Class containing all the settings of the program.

These settings can all be retrieved via the corresponding settings.
"""

import os
import platform

class Settings():
    """ Construct a settings object.

    All settings will be initialized here.
    Some settings depend on which program creates
    the settings object.
    """
    def __init__(self, prg):
        self.primaryColour = "#0000FF"
        self.secondaryColour = "#00FF00"
        self.skipColour = "#FF0000"
        # Zoomfactor
        self.zoom = 4
        # Marking offset
        self.offset = 10
        # Marking width
        self.width = 5

        if prg == "viaduct.py":
            self.indir = "../images"
            self.outdir = "../output"
            self.startat = 1
        elif prg == "distances.py":
            self.indir = "../images"
            self.outdir = "../output"
            self.startat = 1
        elif prg == "vehicles.py":
            self.indir = "../images"
            self.outdir = "../output"
            self.startat = 1
        else:
            self.indir = "../images"
            self.outdir = "../output"
            self.startat = 1

        # Value of the control keys: http://www.asciitable.com/
        # Standard controls are:
        # a: Zoom in and out
        # n: Next picture, and save if clicks are given
        # p: Previous picture, never save
        # s: Skip a marking. Only works in distances.py
        # l: Next lane switch. Only works in distances, and assumes 2 lanes

        # Windows provides keys with the value of the capital key,
        # other systems correctly provide the actual ascii value...
        # This code is horrible, and really needs some proper setup.
        if platform.system() == "Windows":
            self.zoomKey = 65
            self.nextKey = 78
            self.prevKey = 80
            self.skipKey = 83
            self.laneSwitchKey = 76
        else:
            self.zoomKey = 97
            self.nextKey = 110
            self.prevKey = 112
            self.skipKey = 115
            self.laneSwitchKey = 108

    """ Valid image extensions

    Check if a certain image conforms to the extensions we figured.
    """
    def IsValidType(self, ext):
        valid = [".png", ".jpg", ".jpeg", ".bmp"]
        return ext in valid

    """ Return a list of files from a given directory
    
    Technically not a setting, but alas.
    """
    def GetFileList(self, directory):
        return [f for f in os.listdir(directory) if self.IsValidType(os.path.splitext(f.lower())[1])]

    """ Return the zoom factor

    The zoomfactor to use.
    """
    def GetZoomFactor(self):
        return self.zoom

    """ Return the output directory

    The output directory to use.
    """
    def GetOutDir(self):
        return self.outdir

    """ Return the input directory

    The input directory to use.
    """
    def GetInDir(self):
        return self.indir

    """ Return the primary colour

    The primary colour to use.
    """
    def GetPrimaryColour(self):
        return self.primaryColour

    """ Return the secondary colour

    The secondary colour to use.
    """
    def GetSecondaryColour(self):
        return self.secondaryColour

    """ Return the colour to use for skipping markings.

    The colour to use when a marking needs to be skipped.
    """
    def GetSkipColour(self):
        return self.skipColour

    """ Get the zoom keycode

    Return the keycode to use for zooming in.
    """
    def GetZoomKey(self): 
        return self.zoomKey

    """ Get the previous picture keycode

    Return the keycode to use for displaying the previous picture.
    """
    def GetPreviousKey(self): 
        return self.prevKey

    """ Get the next picture keycode

    Return the keycode to use for displaying the next picture.
    """
    def GetNextKey(self): 
        return self.nextKey

    """ Get the skip keycode

    Return the keycode to use for skipping a lane marker point.
    """
    def GetSkipKey(self): 
        return self.skipKey

    """ Get the lane switch keycode

    Return the keycode to use for switching lanes.
    """
    def GetLaneSwitchKey(self): 
        return self.laneSwitchKey

    """ Get the offset of a marking

    Return the marking offset.
    """
    def GetMarkingOffset(self):
        return self.offset

    """ Get the width of a marking

    Return the marking width.
    """
    def GetMarkingWidth(self):
        return self.width

    """ Start at the given file

    Return at which file to start to count.
    """
    def StartAt(self):
        return self.startat
