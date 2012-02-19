# Taken from InfinImage (via wxpython-users mailing list)
""" Conversion convenience class that allows 

different Pil <-> wxPython image conversions.
"""
import wx
from PIL import Image

class Convert():
    """ Convert a bitmap to a PIL image
    """
    def BitmapToPil(self, bitmap):
        return ImageToPil(BitmapToImage(bitmap))

    """ Convert a bitmap to an wx.Image
    """
    def BitmapToImage(self, bitmap):
        return wx.ImageFromBitmap(bitmap)

    """ Convert a wx.Image to a bitmap
    """
    def ImageToBitmap(self, image):
        return image.ConvertToBitmap()

    """ Convert a PIL image to a bitmap
    """
    def PilToBitmap(self, pil):
        return ImageToBitmap(PilToImage(pil))

    """ Convert a PIL image to a wx.Image
    """
    def PilToImage(self, pil):
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        image.SetData(pil.convert('RGB').tostring())
        return image

    """ Convert an wx.Image to a PIL image
    """
    def ImageToPil(self, image):
        pil = Image.new('RGB',(image.GetWidth(), image.GetHeight()))
        pil.fromstring(image.GetData())
        return pil
