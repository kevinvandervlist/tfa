#!/usr/bin/python

# Vehicle program
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

""" Vehicles program.

This program can be used to identify the start and the end of a vehicle's trajectory.
"""

import os
import wx
import inspect

from PIL import Image
from collections import deque

from abstractframe import AbstractFrame
from convert import Convert
from imageoperations import ImageOperations
from logger import Logger
from settings import Settings

class Frame(AbstractFrame):
    def __init__(self, parent=None, id=-1,pos=wx.DefaultPosition, title='wxPython', size=None, settings=None, fileList=[]):
        AbstractFrame.__init__(self, parent, id, pos, title, size, settings, fileList)

    def KeyboardEvent(self, event):
        zk = self.settings.GetZoomKey()
        nk = self.settings.GetNextKey()
        pk = self.settings.GetPreviousKey()

        # zoom
        if event.GetKeyCode() == zk:
            # Toggle zoom
            if self.zoomed:
                self.zoomed = False
                self.SetPilImage()
            else:
                self.zoomed = True
                self.ZoomAtLocation(self.currentMouseLocation)
        elif event.GetKeyCode() == nk:
            if len(self.locationList) > 1:
                self.logger.LogVehicle(self.curFileName, self.locationList)

            self.OpenNextImage()
        elif event.GetKeyCode() == pk:
            self.OpenPrevImage()
        else:
            return

    def MouseEventLeft(self, event):
        if self.zoomed:
            self.zoomed = False
            x = event.GetX()
            y = event.GetY()
            point = self.imops.GetOriginalCoords(self.curZoomLevel, (x,y), self.curViewPort)
            self.imops.SetMarking(self.curPilImage, point, self.settings.GetPrimaryColour())
            self.SetPilImage()
            self.locationList.append(point)

class App(wx.App):
    """ Wx constructor """
    def OnInit(self):
        # Init settings thingy
        settings = Settings(inspect.getfile(inspect.currentframe()))
        # Default size:
        size=(1400, 800)
        # Prepare a list of files to use
        directory = settings.GetInDir()
        im = [directory + os.sep + f for f in settings.GetFileList(directory)]
        im.sort()
        # Setup the frame
        self.frame = Frame(size=size, settings=settings, fileList=im)
        # Finally, show the created frame
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    # Application entrypoint
    app = App()
    app.MainLoop()

