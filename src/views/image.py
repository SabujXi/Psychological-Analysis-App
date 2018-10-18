from .base import BaseView
from Tkinter import (
    Frame,
    Canvas,
    YES,
    BOTH,
    CENTER
)

from PIL import ImageTk
# the view to show the image


class ImageView(BaseView):
    def __init__(self, manager):
        self.viewname = 'imageview'
        BaseView.__init__(self, manager)

    def pack_view(self, *args, **kwargs):
        layout = kwargs.get('layout', 2)
        image_object = kwargs['image_object']
        image_no = kwargs.get('image_no', None)

        left_frame = self.display_left(flexible=True)

        _display_idx = self.manager.get_display_index()
        _display_size = (self.config.DISPLAY_SIZE[_display_idx][0], self.config.DISPLAY_SIZE[_display_idx][1])
        self.manager.log('display size', _display_size)
        self._imgtk = ImageTk.PhotoImage(image_object.resize(_display_size))

        # # self.frame = Frame(self.master)
        # self.frame = Frame(self.master, bg='white', width=_display_size[0], height=_display_size[1])
        # self.frame.grid_propagate(0)
        left_frame.config(bg='white', width=_display_size[0], height=_display_size[1])

        self.canvas = Canvas(left_frame, width=_display_size[0], height=_display_size[1], bg='red')
        # self.canvas.grid_propagate(0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.create_image(2, 2, image=self._imgtk, anchor='nw')
        if image_no is not None:
            self.canvas.create_text(self._imgtk.width() * 0.9, self._imgtk.height() * 0.9, text="Image No: " + str(image_no),
                                fill="white")
        if layout == 2:
            bottom_frame = self.display_bottom(True)

        self.add_next_action_btn(lambda: self.done())
        self.display()
