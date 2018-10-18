"""
Base view to control the view swith between image dispalying, sam and emotion rating views
"""

from Tkinter import (
    Frame,
    N,
    S,
    E,
    W,
    BOTTOM,
    BOTH,
    Button
)
import time

from ttk import Button


class BaseView:
    def __init__(self, manager):
        self.manager = manager
        self.master = manager.root
        self.config = manager.config

        # frames
        self.__display_main_only = False
        self.frame = self.root_frame = Frame(self.master, padx=5, pady=5)
        self.left_frame = self.main_frame = Frame(self.frame)
        self.right_frame = Frame(self.frame)
        self.bottom_frame = Frame(self.frame)
        self.next_button = Button(self.bottom_frame, text='>>', command=lambda: None)
        # self.next_button.place(relx=0.5, rely=0.5, anchor='center')
        # self.next_button.grid(row=0, sticky='n')
        self.next_button.pack(fill='x')

        self.__start_time = None
        self.__end_time = None

        self.__interval_alarm_id = None

    def display_main_only(self):
        assert self.__display_main_only is False
        self.__display_main_only = True

    def display_left(self, flexible=False, row_flexible=True):
        assert self.__display_main_only is False
        self.left_frame.grid(row=0, column=0)
        if flexible:
            self.frame.grid_columnconfigure(0, weight=1)
        if row_flexible:
            self.frame.grid_rowconfigure(0, weight=1)
        return self.left_frame

    def hide_left(self):
        self.left_frame.grid_forget()
        return self.left_frame

    def display_right(self, flexible=False):
        assert self.__display_main_only is False
        self.right_frame.grid(row=0, column=1, sticky=W+E, padx=5, pady=5)
        if flexible:
            self.frame.grid_columnconfigure(1, weight=2)
        return self.right_frame

    def hide_right(self):
        self.right_frame.grid_forget()
        return self.right_frame

    def display_bottom(self, stretch_to_bottom=True):
        assert self.__display_main_only is False
        self.bottom_frame.grid(row=1, column=0, columnspan=2, ipadx=10, ipady=2)
        # if stretch_to_bottom:
        #     self.frame.grid_rowconfigure(1, weight=1)  # commenting this removed the hiding of button in pressure of
        # others
        self.bottom_frame.grid_configure(sticky='se')
        # self.bottom_frame.config(bg='grey')
        # self.bottom_frame.grid_rowconfigure(1, weight=1)
        return self.bottom_frame

    def hide_bottom(self):
        self.bottom_frame.grid_forget()
        return self.bottom_frame

    def add_next_action_btn(self, callback, text='>>', image=None):
        """Adds bottom frame at row 1 and returns nothing"""
        assert callable(callback)
        self.next_button.config(command=callback)
        if text is not None:
            self.next_button.config(text=text)
        if image is not None:
            self.next_button.config(image=image)

    def display(self, expand=True):
        self.__start_time = time.time()
        if expand:
            self.frame.pack(fill=BOTH, expand=1)
        else:
            self.frame.pack()

        # events
        self.register_interval_alarm()

    def stop_interval_alarm(self):
        if self.__interval_alarm_id is not None:
            self.unregister_interval_alarm()

    def unregister_interval_alarm(self):
        if self.__interval_alarm_id is None:
            raise Exception('Cannot unregister as the alarm id is set to None')
        self.frame.after_cancel(self.__interval_alarm_id)
        self.__interval_alarm_id = None

    def register_interval_alarm(self):
        if self.__interval_alarm_id is not None:
            raise Exception('Previous alarm with id `%s` was not unregistered' % str(self.__interval_alarm_id))
        after_id = self.frame.after(1 * 99, self.__after_reported_4_current_view)
        self.__interval_alarm_id = after_id
        return after_id

    def __after_reported_4_current_view(self):
        self.manager.interval_reported_4_current_view()
        self.unregister_interval_alarm()
        self.register_interval_alarm()

    def time_spent(self):
        return self.__end_time - self.__start_time

    def time_spent_until_now(self):
        return time.time() - self.__start_time

    def done(self):
        self.__end_time = time.time()
        self.stop_interval_alarm()
        self.manager.go_next()
