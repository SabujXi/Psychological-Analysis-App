from views import BaseView

from Tkinter import *


class EndView(BaseView):
    """
        The view from where user can start an experiment
    """
    def __init__(self, manager, *args, **kwargs):
        BaseView.__init__(self, manager)

    def pack_view(self, *args, **kwargs):
        info = kwargs.get('info', None)
        left_frame = self.display_left(True)
        lbl = Label(left_frame, text="Experiment Ended!")
        lbl.pack()
        btn_exit = Button(left_frame, text='Exit', command=self.done, width=60, height=10)
        btn_exit.pack()
        if info is not None:
            info_lbl = Label(left_frame, text=info)
            info_lbl.pack()
        self.display()

    def done(self):
        self.manager.destroy()

