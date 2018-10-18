import config
from Tkinter import *
import tkMessageBox as messagebox
from datainput import *
from experiment import *
from device import *
from views import *


class BaseManager(object):
    def __init__(self, root_path, manager_name, *args, **kwargs):
        self.__root_path = root_path
        self.__name = manager_name
        # self.__deferreds = kwargs.get('deferreds', None)
        assert self.__root_path, 'The root path %s does not exist.' % self.__root_path
        self.root = self.master = Tk()
        self.config = config
        self.device = Device(self.config, self)

        self.__views_map = {}
        self.__views_class2name_map = {}
        self.__current_view = None
        self.__init_views()

        # base events
        self.root.bind("<Escape>", lambda e: self.on_closing())
        self.root.bind("<F11>", self.on_key_f11_pressed)

        self.__fullscreen_on = False

    # @property
    # def deferreds(self):
    #     return tuple(self.__deferreds)
    #
    # def add_deferred(self, cl):
    #     assert callable(cl)
    #     if self.__deferreds is not None:
    #         self.__deferreds.append(cl)
    #         print cl, ' deferred added'

    def make_experiment(self, result_dir):
        """
        :param result_dir: relative dir to result that will be resolved with get_path
        :return:
        """
        experiment = Experiment(self.config, self, result_dir)
        return experiment

    def make_input_data(self):
        data_input = DataInput(self.config, self)
        return data_input

    @property
    def root_path(self):
        return self.__root_path

    @property
    def name(self):
        return self.__name

    @property
    def current_view(self):
        return self.__current_view

    def get_path(self, *comps):
        new_path = os.path.join(self.__root_path, *comps)
        # print new_path
        return new_path

    def get_existing_path(self, *comps):
        new_path = self.get_path(*comps)
        assert os.path.exists(new_path), 'The path %s does not exist.' % new_path
        return new_path

    def get_image_object(self, rel_path):
        path = self.get_path(rel_path)
        return Image.open(path)

    def get_image_object_abs(self, abs_path):
        return Image.open(abs_path)

    def __init_views(self):
        """Declare what views will be shown"""
        #  temp_view_4_technique_four = TempViewForTechniqueFour(config, objects, root)
        #  temprature_only_view = TempView(config, objects, root)
        self._add_view('start_view', StartView)
        self._add_view('information_view', InformationView)
        self._add_view('image_view', ImageView)
        self._add_view('sam_view', SamView)
        self._add_view('text_box_view', TextBoxView)
        self._add_view('selection_view', SelectionView)
        self._add_view('end_view', EndView)

    def _add_view(self, view_name, view_class):
        assert issubclass(view_class, BaseView)
        assert view_name not in self.__views_map
        self.__views_map[view_name] = view_class
        self.__views_class2name_map[view_class] = view_name

    def get_view_name_by_class(self, view_class, default=None):
        try:
            return self.__views_class2name_map[view_class]
        except:
            return default

    def get_view_class_by_name(self, view_name, default=None):
        try:
            return self.__views_map[view_name]
        except:
            return default

    def create_view(self, name, *args, **kwargs):
        view_class = self.get_view_class_by_name(name)
        return view_class(self)

    def start_view(self, view, *args, **kwargs):
        self._end_current_view()
        self.__current_view = view
        view.pack_view(*args, **kwargs)
        return view

    def create_start_view(self, name, *args, **kwargs):
        return self.start_view(self.create_view(name), *args, **kwargs)

    def _end_current_view(self):
        current_view = self.__current_view
        if self.__current_view is not None:
            view = self.__current_view
            view.frame.forget()
            view.frame.destroy()
            self.__current_view = None
            print "Current view ended"
        return current_view

    def run(self, *args, **kwargs):
        self.root.title("Experiment")
        self.root['background'] = 'white'
        max_display_size = self.config.DISPLAY_SIZE[2]
        self.root.geometry(str(max_display_size[0]) + 'x' + str(max_display_size[1]))

        #  Experiment is to hold all the experiment data, such as image number, rating info
        # self.create_start_view(first_view)
        self.go_next()
        self.root.mainloop()

    def destroy(self):
        self._end_current_view()
        self.root.destroy()
        self.root.quit()

    def go_next(self):
        """This method should be overridden for each manager"""
        print 'gonext called'
        return self._end_current_view()

    def interval_reported_4_current_view(self):
        """Override this method in implemented managers to know about time."""
        # time_passed = self.current_view.time_spent_until_now()
        # print 'interval_reported_4_current_view(): Time passed: ', time_passed

    def on_key_f11_pressed(self, *args, **kwargs):
        self.toggle_fullscreen()

    def toggle_fullscreen(self, *args, **kwargs):
        if self.__fullscreen_on is True:
            print 'f pressed: fullscreen mode is on and turning off now'
            self.master.attributes("-fullscreen", False)
            self.__fullscreen_on = False
        else:
            print 'f pressed: fullscreen mode is off and turning on now'
            self.master.attributes("-fullscreen", True)
            self.__fullscreen_on = True

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # self.dataManager.save()
            self.destroy()
        else:
            pass

    def get_display_index(self):
        # _dataIndex = self.selection_indexes[self.count]
        # _temp_idx = self.experiment_data[_dataIndex][2]
        # return self.tempratures[_temp_idx][1]
        return 2  # Large display by default

    @staticmethod
    def next_in_serial(current, a_list):
        """
            returns: next value, was previous value at the end of the list
        """
        cidx = None
        try:
            cidx = a_list.index(current)
        except ValueError:
            raise Exception('No view named `%s` found in `%s`' % (str(current), str(a_list)))
        if cidx == len(a_list) - 1 and len(a_list) != 1:
            return a_list[0], True
        elif len(a_list) == 1:
            return a_list[0], True
        else:
            return a_list[cidx + 1], False

    @classmethod
    def get_base_fn_wo_ext(cls, fn):
        fn_wo_ext = cls.get_path_wo_ext(fn)
        base_fn_wo_ext = os.path.basename(fn_wo_ext)
        return base_fn_wo_ext

    @classmethod
    def get_path_wo_ext(cls, path):
        path_wo_ext = '.'.join(path.rsplit('.', 1)[:-1])
        return path_wo_ext

