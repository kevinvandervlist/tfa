# Logger
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

""" Logger class to output relevant data about the lists of locations retrieved from the user.

This class is _NOT_ a generic logger. It is tailored to output data in specific filenames, and in specific formats.
"""

import io
import sys
import os

class Logger():
    """ Initialize the loggor
    
    Set a local reference to the settings class.
    """
    def __init__(self, settings):
        self.settings = settings

    """ Get a filename to use for output.
    
    This function is used to create a valid filename of the logfile, 
    based on a header and the current image filename in use.
    """
    def GetFileName(self, header, raw_fn):
        outdir = self.settings.GetOutDir()
        fileout = header + os.path.splitext(os.path.basename(raw_fn))[0] + ".txt"
        return outdir + os.sep + fileout

    """ Write a given buffer to a certain log file.
    
    Write the given buffer to the filename at the given location.
    If a file exists, it's content will be truncated.
    """

    def WriteLog(self, log, buf):
        fh = open(log, 'w')
        fh.write(buf)
        fh.close()

    """ Generic logging function.
    
    Log a certain list with locations to a given file. 
    Prepend the logfile with the string given in header.
    """
    def GenericLog(self, header, filename, loclist):
        fhs = self.GetFileName(header, filename)
        
        buf = ""
        for x in loclist:
            if x == 0:
                # Invalid marking
                buf += str(x) + " " + str(x) + " "
            else:
                buf += str(x[0]) + " " + str(x[1]) + " "

        self.WriteLog(fhs, buf + "\n")

    """ The logging function for the viaduct program.

    Log with a certain prefix.
    """
    def LogViaduct(self, filename, loclist):
        self.GenericLog("RV#", filename, loclist)

    """ The logging function for the vehicle program.

    Log with a certain prefix.
    """
    def LogVehicle(self, filename, loclist):
        self.GenericLog("TS#", filename, loclist)

    """ The logging function for the distances program.

    The loclist is split in two, and the two lists wil be made of equal length.
    This will be done by appending zeroes until they are of the same length.
    """

    def LogDistances(self, filename, loclist):
        fhs = self.GetFileName("Di#", filename)
        buf = ""
        lane_a = []
        lane_b = []
        cur_lane = lane_a
        # This for-loop Leaves a trailing space.
        for x in loclist:
            if x == 0:
                # Invalid marking
                cur_lane.append((0, 0))
            elif x == -1:
                # New lane
                cur_lane = lane_b
            else:
                cur_lane.append(x)

        # Fill so both lists have the same number of entries
        while(len(lane_b) > len(lane_a)):
            lane_a.append((0, 0))
            
        while(len(lane_a) > len(lane_b)):
            lane_b.append((0, 0))

        for a in lane_a:
            buf += str(a[0]) + " " + str(a[1]) + " "
        buf += "\n"
        for b in lane_b:
            buf += str(b[0]) + " " + str(b[1]) + " "

        self.WriteLog(fhs, buf + "\n")
