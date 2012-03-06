#!/usr/bin/python

# Abstract program frame class. 
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

""" Abstract program frame class.

Extend and override the eventlisteners to create a new program.
The following eventlisteners are available:

    KeyboardEvent
    MouseEventLeft
    MouseEventRight

In this base class, they just return.
"""

import inspect
import os
import platform
import wx

from PIL import Image
from collections import deque

from settings import Settings
from logger import Logger
from convert import Convert
from imageoperations import ImageOperations

class AbstractFrame(wx.Frame):
    """ Initialize data needed to allow the frame to work.

    Included are lists with image names, viewport sizes, etc.
    """
    def __init__(self, parent=None, id=-1,pos=wx.DefaultPosition, title='wxPython', size=None, settings=None, fileList=[]):
        self.imops = ImageOperations()
        # A conversion object is needed for pil <-> wx
        self.convert = Convert()
        # Store size info of the current window. 2-tuple
        self.size = size
        # The given settings
        self.settings = settings
        # Logger
        self.logger = Logger(settings)
        # And data about the current image
        self.curZoomLevel = None
        self.curViewPort = None
        self.curPilImage = None
        self.curWxImage = None
        self.curScaledImage = None
        self.bitmap = None
        self.todoFileList = deque(fileList)
        self.doneFileList = deque([])
        self.zoomed = False
        self.curFileName = None
        self.locationList = []
        self.skip = False
        self.colour = None
        # Init frame
        style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER)

        wx.Frame.__init__(self, parent, id, title, pos, size, style=style)
        # Panel to allow Linux to have keypress events as well.
        self.panel = wx.Panel(self, wx.ID_ANY)
        # And explicitly request focus for the same reason
        self.panel.SetFocus()

        if platform.system() == 'Windows':
            self.panel.Bind(wx.EVT_KEY_DOWN, self.KeyboardEvent)
        else:
            self.Bind(wx.EVT_CHAR_HOOK, self.KeyboardEvent)

        # Finally, start the image loop
        self.OpenNextImage()

    """ Load an image file.

    Load up an imagefile, and make sure it gets displayed. 
    Eventlisteners are (re)binded as well.
    """
    def LoadImageFile(self, imageFile):
        # Update titlebar with current filename and a position counter.
        self.SetTitle("File: " + imageFile + ": " + str(len(self.doneFileList)) + "/" + str(len(self.todoFileList) + len(self.doneFileList)))
        # Reset internal data
        self.curZoomLevel = 1
        self.curPilImage = Image.open(imageFile)
        self.SetPilImage()
        # Redraw stuff
        self.panel.Layout()
        self.panel.Refresh()
        self.Layout()
        self.Refresh()


    """ Attach the correct mouselisteners to the current bitmap

    Use whon a bitmap is destroyed, and a new one is attached to the frame.
    """
    def AttachListenersToBitmap(self):
        # Mouse events have to be attached to the bitmap
        self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.MouseEventLeft)
        self.bitmap.Bind(wx.EVT_RIGHT_DOWN, self.MouseEventRight)
        self.bitmap.Bind(wx.EVT_MOTION, self.SetMouseLocation)

    """ Set the current PIL image as bitmap image.

    In other words, display the current PIL image on the gui.
    If there exists a bitmap, destroy it first.
    """
    def SetPilImage(self):
        self.curWxImage = self.convert.PilToImage(self.curPilImage)
        self.curScaledImage = self.imops.ScaleWxImage(self.curWxImage, self.size)
        self.curScaledImageSize = (self.curScaledImage.GetWidth(), self.curScaledImage.GetHeight())
        self.curViewPort = (0, 0, self.curScaledImageSize[0], self.curScaledImageSize[1])

        if self.bitmap:
            self.bitmap.Destroy()

        bm = self.curScaledImage.ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(parent=self.panel, pos=(0,0), bitmap=bm, size=bm.Size)

        self.AttachListenersToBitmap()

    """ Zoom in at the given location

    Zoom in an given location (x, y), and redraw the screen.
    """
    def ZoomAtLocation(self, location):
        self.curZoomLevel = self.settings.GetZoomFactor()
        self.curViewPort = self.imops.CalculateViewPort(self.curZoomLevel, location, self.curPilImage.size, self.curScaledImageSize)

        crop = self.convert.PilToImage(self.curPilImage.crop(self.curViewPort))
        crop_sc = self.imops.ScaleWxImageForced(crop, self.size)

        if self.bitmap:
            self.bitmap.Destroy()

        bm = crop_sc.ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(parent=self.panel, pos=(0,0), bitmap=bm, size=bm.Size)

        self.AttachListenersToBitmap()

    """ Iterate to the next image (if any).
    
    Go to the next image. If there aren't any images left, destroy the frame and it's resources.
    Also update the done/todo file lists, so iterating through the images is possible.
    """
    def OpenNextImage(self):
        self.colour = self.settings.GetPrimaryColour()
        if len(self.todoFileList) == 0:
            self.Destroy()
        else:
            if self.curFileName != None:
                self.doneFileList.append(self.curFileName)
            cur = self.todoFileList.popleft()
            self.curFileName = cur
            self.locationList = []
            self.LoadImageFile(cur)

    """ Iterate to the previous image (if any).
    
    Go to the previous image, if it exists.
    Also update the done/todo file lists, so iterating through the images is possible.
    """
    def OpenPrevImage(self):
        if len(self.doneFileList) == 0:
            return
        else:
            if self.curFileName != None:
                self.todoFileList.appendleft(self.curFileName)
            cur = self.doneFileList.pop()
            self.curFileName = cur
            self.locationList = []
            self.LoadImageFile(cur)

    """ Default KeyboardEvent listener
    
    Override it to change behavior of this abstract frame.
    It currently does nothing.
    """
    def KeyboardEvent(self, event):
        return

    """ Default MouseEventLeft listener
    
    Override it to change behavior of this abstract frame.
    It currently does nothing.
    """
    def MouseEventLeft(self, event):
        return

    """ Default MouseEventRight listener
    
    Override it to change behavior of this abstract frame.
    It currently does nothing.
    """
    def MouseEventRight(self, event):
        return

    """ Stores the current mouse position on the frame.

    Stores the current mouse position on the active frame. Used
    for zooming in.
    """
    def SetMouseLocation(self, event):
        self.currentMouseLocation = (event.GetX(), event.GetY())
