from .base import BaseView

from Tkinter import (
    Label,
    CENTER
)

from PIL import (
    Image,
    ImageTk
)

from src.resource import (
    CTR,
    ACT,
    VAL
)

from .misc import TagLabel
from collections import namedtuple

SamSelection = namedtuple('SamSelection', ('catetory', 'tag_value', 'widget'))


class SamView(BaseView):
    def __init__(self, manager):
        self.viewname = 'Sam view'
        BaseView.__init__(self, manager)

        self.load_resource()
        self.selections = {}

    def load_resource(self):
        self.background_sam = Image.open("resource/sam.jpg")
        (self.sam_width, self.sam_height) = self.background_sam.size
        self.background_sam.thumbnail(self.background_sam.size)
        self.sam_bg_img = ImageTk.PhotoImage(self.background_sam)

        self.off = Image.open("resource/off.jpg")
        self.off.thumbnail(self.off.size)
        self.off_img = ImageTk.PhotoImage(self.off)

        self.on = Image.open("resource/on.jpg")
        self.on.thumbnail(self.on.size)
        self.on_img = ImageTk.PhotoImage(self.on)

    def sam_button_action(self, event=None):
        widget = event.widget
        catetory = widget.catetory
        tag = widget.tag

        if catetory in self.selections:
            _selection = self.selections[catetory]
            _selection.widget['image'] = self.off_img

        widget['image'] = self.on_img

        selection = SamSelection(catetory=catetory, tag_value=tag, widget=widget)
        self.selections[catetory] = selection

    def get_selections(self):
        res = {}
        for selection in self.selections.values():
            res[selection.catetory] = str(selection.tag_value)

        for key in ('activation', 'valence', 'control'):
            if key not in res:
                res[key] = ''
        return res

    def pack_view(self, *args, **kwargs):
        layout = kwargs.get('layout', 2)
        image_object = kwargs.get('image_object', None)
        self.selections = {}
        left_frame = self.display_left(True)
        left_frame.config(width=self.sam_width, height=self.sam_height)

        self._prepare_sam(left_frame)

        # adding preview image
        if layout == 3:
            right_frame = self.display_right(True)
            self._prev_img = ImageTk.PhotoImage(image_object)
            self._prev = Label(right_frame, image=self._prev_img)
            self._prev.place(relx=0.5, rely=0.5, anchor=CENTER)
            right_frame.config(width=self.sam_width, height=self.sam_height)

        # adding next button
        if layout in (2, 3):
            bottom_frame = self.display_bottom()
            self.add_next_action_btn(self.on_next_click)

        self.display()

    def _prepare_sam(self, left_frame):
        lbl = Label(left_frame, image=self.sam_bg_img, borderwidth=0)
        lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

        for i in range(0, 9):
            lbl = TagLabel(left_frame, i + 1, 'valence', 'val_lbl%d' % i, image=self.off_img)
            setattr(self, 'val_lbl%d' % i, lbl)
            getattr(self, 'val_lbl%d' % i).bind('<Button-1>', self.sam_button_action)
            getattr(self, 'val_lbl%d' % i).place(relx=(i * 1.0) * (VAL['X1'] - VAL['X0']) / 8.0 + VAL['X0'],
                                                 rely=VAL['Y'], anchor=CENTER)

            lbl = TagLabel(left_frame, i + 1, 'activation', 'act_lbl%d' % i, image=self.off_img)
            setattr(self, 'act_lbl%d' % i, lbl)
            getattr(self, 'act_lbl%d' % i).bind('<Button-1>', self.sam_button_action)
            getattr(self, 'act_lbl%d' % i).place(relx=(i * 1.0) * (ACT['X1'] - ACT['X0']) / 8.0 + ACT['X0'],
                                                 rely=ACT['Y'], anchor=CENTER)

            lbl = TagLabel(left_frame, i + 1, 'control', 'ctr_lbl%d' % i, image=self.off_img)
            setattr(self, 'ctr_lbl%d' % i, lbl)
            getattr(self, 'ctr_lbl%d' % i).bind('<Button-1>', self.sam_button_action)
            getattr(self, 'ctr_lbl%d' % i).place(relx=(i * 1.0) * (CTR['X1'] - CTR['X0']) / 8.0 + CTR['X0'],
                                                 rely=CTR['Y'], anchor=CENTER)

    def on_next_click(self):
        self.done()

