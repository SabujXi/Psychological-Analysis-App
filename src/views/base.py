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

from tkinter.ttk import Button


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
        print 'callback for button: ', callback
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
        print 'Done called'
        self.__end_time = time.time()
        self.stop_interval_alarm()
        self.manager.go_next()

# --------------------------------------------------------------
    # def setExperimentData(self):
    #     return
    #     #  temperatures = data_obj.getTempraturesOfCurrentTech()[0:5]
    #     #  expe_data = str(temperatures[0])+':'+str(temperatures[1])+':'+str(temperatures[2])+':'
    #     #  +str(temperatures[3])+':'+str(temperatures[4])
    #     _expe_data = str(self.data_input.get_temperature())
    #     print 'set experiment data ', _expe_data
    #     self.experiment.data[self.experiment.count]['temperature'] = _expe_data
    #
    #     _display_idx = self.data_input.get_display_index()
    #     _display_details = self.config.DISPLAY[_display_idx]
    #     print 'display index=%d _display_details=%s' % (_display_idx, _display_details)
    #     self.experiment.data[self.experiment.count]['display_size'] = _display_details
    #
    # def goNextView(self):
    #     return
    #     self.frame.pack_forget()
    #     self.frame.destroy()
    #
    #     _lastviewname = self.viewname
    #     if _lastviewname == 'emotionview':
    #         self.setExperimentData()
    #
    #         self.experiment.count += 1
    #         self.pauseBtn.pack_forget()
    #         self.pauseBtn.destroy()
    #
    #     if self.experiment.is_finished():
    #         self.experiment.save()
    #         self.experiment.reset()
    #         self.start_view.packView()
    #         print 'go back to start view'
    #         return
    #
    #     if _lastviewname == 'emotionview':
    #         print '[', self.experiment.count, '] images have been shown'
    #         print ''
    #         self.experiment.save()
    #         self.data_input.move_to_next_data()
    #     self.nextView.packView()

