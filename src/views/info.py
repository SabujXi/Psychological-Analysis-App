from .base import BaseView

from Tkinter import (
    Frame,
    Label
)

from ttk import *


class InformationView(BaseView):
    def __init__(self, manager):
        self.viewname = 'informationView'
        BaseView.__init__(self, manager)

    def pack_view(self, *args, **kwargs):
        # TODO: adapt new architecture
        self.frame = Frame(self.master, width=1024, height=768)
        self.frame.grid_propagate(0)
        text = Label(self.frame, width=1024, height=768, text=self.config.EXPERIMENT['INFORMATION_TEXT'])
        self.frame.pack()
        text.pack()
        # self.device.reset_temperature()


