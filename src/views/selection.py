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

    Checkbutton,
    IntVar,
    Canvas,
    DISABLED
)

from tkinter.ttk import (
    Button,
    Label,
    Radiobutton,
)

from PIL import (
    Image,
    ImageTk
)


class SelectionView(BaseView):
    def __init__(self, manager):
        self.viewname = 'selectionView'
        BaseView.__init__(self, manager)

        self.__temp_values = [26, 29, 35, 38]
        self.__temps_editable_text = ['Very Cool', 'Cool', 'Warm', 'Very Warm']

        self.__var_rdo = IntVar()
        self.__var_rdo.set(-1)
        self.__var_rdo.trace_variable("w", self.var_rdo_changed)

    def pack_view(self, *args, **kwargs):
        layout = kwargs.get('layout', 2)
        image_object = kwargs['image_object']
        image_no = kwargs.get('image_no', None)

        temps_string = [str(value) + 'C' for value in self.__temp_values]  # ['26C', '29C', '35C', '38C']
        temps_editable_text = self.__temps_editable_text
        left_frame = self.display_left(False)

        rdo1 = Radiobutton(left_frame, variable=self.__var_rdo, value=0)
        rdo2 = Radiobutton(left_frame, variable=self.__var_rdo, value=1)
        rdo3 = Radiobutton(left_frame, variable=self.__var_rdo, value=2)
        rdo4 = Radiobutton(left_frame, variable=self.__var_rdo, value=3)

        radio_buttons = [rdo1, rdo2, rdo3, rdo4]
        idx = 0
        for radio_button in radio_buttons:
            radio_button.grid(row=idx, column=0, ipady=10)
            idx += 1

        btn1 = Button(left_frame, text=temps_string[0], command=lambda *args: self.__var_rdo.set(0))
        btn2 = Button(left_frame, text=temps_string[1], command=lambda *args: self.__var_rdo.set(1))
        btn3 = Button(left_frame, text=temps_string[2], command=lambda *args: self.__var_rdo.set(2))
        btn4 = Button(left_frame, text=temps_string[3], command=lambda *args: self.__var_rdo.set(3))

        push_buttons = [btn1, btn2, btn3, btn4]
        idx = 0
        for push_button in push_buttons:
            push_button.grid(row=idx, column=1, ipady=5, ipadx=10)
            idx += 1

        lbl1 = Label(left_frame, text=temps_editable_text[0])
        lbl2 = Label(left_frame, text=temps_editable_text[1])
        lbl3 = Label(left_frame, text=temps_editable_text[2])
        lbl4 = Label(left_frame, text=temps_editable_text[3])

        labels = [lbl1, lbl2, lbl3, lbl4]
        idx = 0
        for label in labels:
            label.grid(row=idx, column=2, ipady=5)
            idx += 1

        # ROW & COLUMN CONFIGURE
        for row in range(4):
            left_frame.rowconfigure(row, weight=2, pad=10)  # row: 0, 1, 2, 3
        for column in range(3):
            left_frame.columnconfigure(column, weight=2, pad=5)  # column: 0, 1, 2

        # image and button
        # adding preview image
        if layout == 3:
            right_frame = self.display_right(True)
            self._prev_img = ImageTk.PhotoImage(image_object)
            self._prev = Label(right_frame, image=self._prev_img)
            self._prev.pack(fill=BOTH, expand=YES, anchor=CENTER)

        # adding next button
        if layout in (2, 3):
            bottom_frame = self.display_bottom(False)
            self.add_next_action_btn(self.on_next_click)

        # Default Radio Selection
        # rdo1.select()
        # rdo1.invoke()
        # print(self.master.winfo_screenwidth())
        self.display()

    def var_rdo_changed(self, *args):
        # print args
        idx = self.__var_rdo.get()
        temp = self.__temp_values[idx]
        self.manager.set_temp_for_sec(temp, 6)

    def on_next_click(self):
        self.done()

    def get_temp_value(self):
        """
        :return: integer value of temperature. By default 32 is returned.
        """
        value = self.__var_rdo.get()
        if value in (0, 1, 2, 3):
            temp = self.__temp_values[value]
        else:
            temp = 32
        return temp

