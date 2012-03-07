# ImageOperations
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

""" The ImageOperations class is used to manipulate images used in the programs.

This class is used to do most of the image-related work.
It can be used to return a (zoomed in) viewport of an image, 
set markers on certan (x,y) locations, or translate (x,y) locations
to real coordinates inside the source image.
"""
import wx

from PIL import Image
from PIL import ImageDraw
from convert import Convert

class ImageOperations():
    """ Return a viewport.
    
    Calculated based on the zoomlevel and location 2-tuple (x,y) of mousepointer
    Returning 4-tuple is (left, up, right, bottom) coords of the viewport
    """
    def CalculateViewPort(self, zoom, location, orgsize, scalesize):
        # Don't exceed app size
        view_width = scalesize[0] / zoom
        view_height = scalesize[1] / zoom
        # Map the coords
        location_mapped = self.GetOriginalCoordFromScaledCoord(location, orgsize, scalesize)
        x = location_mapped[0]
        y = location_mapped[1]
        # And calculate the four specific boundaries based on mapped coords
        left = x - view_width / 2
        right = x + view_width / 2
        up = y - view_height / 2
        bottom = y + view_height / 2

        return self.ValidateViewport(left, up, right, bottom)

    """ Validate a given viewport.

    A viewport can be invalid for a number of reasons. 
    Validate it inside this function, for example because 
    the upper and bottom region are the same digit.
    """
    def ValidateViewport(self, left, up, right, bottom):
        if left == right:
            left -= 100
            right += 100
        if up == bottom:
            up -= 100
            bottom += 100
        return (left, up, right, bottom)

    """ Return the (x, y) location of a mousclick in a viewport.

    Return the real (x, y) coords in an image, based on a (x, y) location
    in a specific viewport. 
    """
    def GetOriginalCoords(self, zoom, location, curviewport):
        unzoomedLocationX = location[0] / zoom + curviewport[0]
        unzoomedLocationY = location[1] / zoom + curviewport[1]

        return (unzoomedLocationX, unzoomedLocationY)

    """ Map scaled coords to original
    
    Return a 2-tuple (x, y) with the coordinates in the original image.
    This is based on the given coords of the scaled image.
    """
    def GetOriginalCoordFromScaledCoord(self, location, org, scale):
        x = location[0] * org[0] / scale[0]
        y = location[1] * org[1] / scale[1]
        return (x, y)

    """ Forcibly scale an image

    Always return a scaled image, even if it means upscaling.

    When the resulting scaling < 1, make sure it is still at least a pixel high.
    """
    def ScaleWxImageForced(self, wximage, size):
        x = wximage.GetWidth()
        y = wximage.GetHeight()

        xfac = float(x) / float(size[0])
        yfac = float(y) / float(size[1])
        xn = 0
        yn = 0

        if xfac >= yfac:
            xn = x / xfac
            yn = y / xfac
        else:
            xn = x / yfac
            yn = y / yfac

        if xn < 1:
            xn += 1

        if yn < 1:
            yn += 1

        return wximage.Scale(xn, yn)


    """ Scale an image

    Return a scaled image, so images > the current screen fit it there.
    If image is < size; return an unmodified image
    """
    def ScaleWxImage(self, wximage, size):
        W = wximage.GetWidth()
        H = wximage.GetHeight()

        # If the size > image, don't scale.
        if size[0] > W and size[1] > H:
            return wximage
        else:
            return self.ScaleWxImageForced(wximage, size)

    """ Set a marking at a given point.
    
    The marking is a little box around a given point (x, y) 
    that will be painted on the PIL image pilimg.
    """
    def SetMarking(self, pilimg, point, colour, offset, width):
        draw = ImageDraw.Draw(pilimg)

        top = (point[0] - offset, point[1] - offset, point[0] + offset, point[1] - offset)
        left = (point[0] - offset, point[1] - offset, point[0] - offset, point[1] + offset)
        right = (point[0] + offset, point[1] - offset, point[0] + offset, point[1] + offset)
        bottom = (point[0] - offset, point[1] + offset, point[0] + offset, point[1] + offset)

        draw.line(top, fill=colour, width=width)
        draw.line(left, fill=colour, width=width)
        draw.line(right, fill=colour, width=width)
        draw.line(bottom, fill=colour, width=width)
        del draw
