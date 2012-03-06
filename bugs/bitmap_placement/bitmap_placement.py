#!/usr/bin/python

import wx

class Frame(wx.Frame):
    def __init__(self):

        title="bitmap placement issue"
        pos=(0, 0)
        size=(320, 240)

        wx.Frame.__init__(self, parent=None, title=title, pos=pos, size=size)

        bm = wx.BitmapFromImage(wx.Image("bitmap_placement.png", wx.BITMAP_TYPE_PNG))
        
        self.bitmap = wx.StaticBitmap(parent=self, pos=pos, bitmap=bm, size=size)

class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()
