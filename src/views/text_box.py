from .base import BaseView

from Tkinter import (
    Label,
    Text,
    RIDGE,
    FLAT,
    SUNKEN,
    RAISED,
    GROOVE,
    CENTER,
    W,
    E,
    S,
    N,
    BOTH,
    YES,
    Button,
    Radiobutton,
    Checkbutton,
    IntVar,
    Canvas
)


from PIL import (
    Image,
    ImageTk
)


class TextBoxView(BaseView):
    def __init__(self, manager):
        self.viewname = 'textboxView'
        BaseView.__init__(self, manager)
        self.__text = ''

    def get_text(self):
        return self.__text

    def pack_view(self, *args, **kwargs):
        layout = kwargs.get('layout', 2)
        image_object = kwargs.get('image_object', None)

        left_frame = self.display_left(True)
        # text box
        self._lbl = Label(left_frame, text='Text Box')
        self._text_widget = Text(left_frame)
        self._text_widget.config(bd=5, relief=RIDGE)
        self._lbl.pack(expand=1)
        self._text_widget.pack(expand=1)

        # image and button
        # adding preview image
        if layout == 3:
            right_frame = self.display_right(True)
            self._prev_img = ImageTk.PhotoImage(image_object)
            self._prev = Label(right_frame, image=self._prev_img)
            # self._prev.place(relx=0.5, rely=0.5, anchor=CENTER)
            # self._prev.place(relx=0.5, rely=0.5, anchor=CENTER)
            # self._prev.grid(row=0, sticky=W+E)
            self._prev.pack(fill=BOTH, expand=YES, anchor=CENTER)

        # adding next button
        if layout in (2, 3):
            bottom_frame = self.display_bottom(False)
            self.add_next_action_btn(self.on_next_click)

        # left_frame.config(width=self.sam_width, height=self.sam_height)
        # right_frame.config(width=500, height=500)
        self.display()

    def on_next_click(self):
        self.__text = self._text_widget.get("1.0", "end-1c")
        self.done()


