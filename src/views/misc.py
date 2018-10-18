from Tkinter import (
    Label
)

from tkinter.ttk import *


class TagLabel(Label):
    def __init__(self, master, tag, catetory, name, rx=None, ry=None, lblbg=None, image=None, text=None, takefocus=None):
        Label.__init__(self, master, image=image, text=text, borderwidth=0, takefocus=takefocus)
        self.tag = tag
        self.name = name
        self.catetory = catetory
        self.lblbg = lblbg
        self.rx=rx
        self.ry=ry
