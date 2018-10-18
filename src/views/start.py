from views import BaseView

from Tkinter import *


class StartView(BaseView):
    """
        The view from where user can start an experiment
    """
    def __init__(self, manager, *args, **kwargs):
        BaseView.__init__(self, manager)

    def pack_view(self, *args, **kwargs):
        left_frame = self.display_left(True)
        self.btn = Button(left_frame, text='Start', command=self.done, width=60, height=10)
        self.btn.pack()
        self.display()

