import os
import random
from .base_manager import BaseManager
from .three import ManagerThree


class ManagerTwo(BaseManager):
    def __init__(self, root_path, name, *args, **kwargs):
        super(self.__class__, self).__init__(root_path, name, *args, **kwargs)

        self.__images_to_display = []
        self.__total_images = 0
        self.__root_images_dirname = os.path.join('images', self.name)

        self.__experiment = self.make_experiment(os.path.join('results', self.name))
        self.__current_image_fn = None

        self.__data = {}
        self._reset_data()

        self.__current_temp_after_id = None

    def _reset_data(self):
        res = {}
        for key in (
                'image_fn_base',
                'temperature',
                'valence',
                'activation',
                'control',
                'text',
                'time_on_image',
                'time_on_rating',
                'time_on_text'):
            res[key] = ''
        self.__data = res

    def add_row(self):
        if any(self.__data.values()):
            row = [
                self.__data['image_fn_base'],
                self.__data['temperature'],
                self.__data['valence'],
                self.__data['activation'],
                self.__data['control'],
                self.__data['text'],
                self.__data['time_on_image'],
                self.__data['time_on_rating'],
                self.__data['time_on_text']
            ]
            for i, v in enumerate(row):
                row[i] = str(v)
            self.__experiment.add_row(row)
            self._reset_data()

    def run(self, *args, **kwargs):
        self.__populate_random_images()
        self.__images_to_display_bk = list(self.__images_to_display)
        self.__images2temps = dict((fn, 32) for fn in self.__images_to_display_bk)
        self.__experiment.start()
        headers = ['image_name', 'temperature', 'valence', 'activation', 'control', 'text',
                   'time_on_image', 'time_on_rating', 'time_on_text']
        self.__experiment.add_row(headers)
        super(self.__class__, self).run(*args, **kwargs)

    def __populate_random_images(self):
        images_sub_dirs = [subdir for subdir in os.listdir(self.get_path(self.__root_images_dirname))
                           if os.path.isdir(self.get_path(self.__root_images_dirname, subdir))]

        files = []

        for images_sub_dir in images_sub_dirs:
            images_sub_dir_abs = self.get_path(self.__root_images_dirname, images_sub_dir)
            assert os.path.exists(images_sub_dir_abs), 'Images directory could not be found: %s' % images_sub_dir_abs

            _files = []
            for fn in os.listdir(images_sub_dir_abs):
                rel_fn = os.path.join(self.__root_images_dirname, images_sub_dir, fn)
                # filter images
                full_fn = self.get_path(rel_fn)
                if os.path.isfile(full_fn) and fn.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp')):
                    _files.append(rel_fn)
            _half_no = len(_files) / 2
            random.shuffle(_files)
            _half_files = _files[:_half_no]
            files.extend(_half_files)

        # filtering out images: in this manager filtering is done above.
        image_fns = []
        for fn in files:
            image_fns.append(fn)

        self.__images_to_display = image_fns

        random.shuffle(self.__images_to_display)
        self.__total_images = len(self.__images_to_display)

    def go_next(self):
        # prev_view name
        # setting current view name
        prev_view = super(self.__class__, self).go_next()
        prev_view_name = None
        current_view_name = None
        current_view = None
        if prev_view is not None:
            prev_view_name = self.get_view_name_by_class(prev_view.__class__, None)

        # display end if no more image is left. end app if total images is zero
        if self.__total_images == 0:
            self.create_start_view('end_view', info='No images found in the folder')
            return

        # view switching
        if prev_view_name is None:
            current_view = self.create_start_view('start_view')
        elif prev_view_name == 'start_view' or prev_view_name == 'text_box_view':
            # no more starting game
            if len(self.__images_to_display) > 0:
                self.__current_image_fn = image_fn = self.__images_to_display.pop()
                self.__image_object = self.get_image_object(image_fn)
                self.__image_no = self.__total_images - len(self.__images_to_display)
                current_view = self.create_start_view('selection_view', layout=3, image_object=self.__image_object, image_no=self.__image_no)
            else:  # end of presentation
                current_view = self.create_start_view('end_view', info='All images displayed. Exit to start Playback.')
        elif prev_view_name == 'selection_view':
            current_view = self.create_start_view('sam_view', layout=3, image_object=self.__image_object, image_no=self.__image_no)
        elif prev_view_name == 'sam_view':
            current_view = self.create_start_view('text_box_view', layout=3, image_object=self.__image_object, image_no=self.__image_no)
        else:
            # e.g. end view
            self.destroy()

        # data collection
        if current_view is not None:
            current_view_name = self.get_view_name_by_class(current_view.__class__)

        if prev_view_name != 'start_view':
            if prev_view_name == 'selection_view':
                # data
                self.__data['image_fn_base'] = self.get_base_fn_wo_ext(self.__current_image_fn)
                self.__data['temperature'] = prev_view.get_temp_value()
                self.__data['time_on_image'] = prev_view.time_spent()
            elif prev_view_name == 'sam_view':
                self.__data['time_on_rating'] = prev_view.time_spent()
                selections = prev_view.get_selections()
                self.__data['valence'] = selections['valence']
                self.__data['activation'] = selections['activation']
                self.__data['control'] = selections['control']
            elif prev_view_name == 'text_box_view':
                self.__data['text'] = prev_view.get_text()
                self.__data['time_on_text'] = prev_view.time_spent()
                self.add_row()
            elif prev_view_name == 'end_view':
                self.__experiment.end()

        # temperature setting
        self.device.set_temperature(32)  # set temperature to 32C as the default temperature whenever view changes.

        self.__cancel_if_temp_after_running()
        return current_view

    def __cancel_if_temp_after_running(self):
        """
        Every time user select a temperature from the temperature selection, it is presented to the device for 6s.
        User might select another temperature in that duration. On selecting another temperature the timer for 6s must
        be cancelled. That's what this method does.
        """
        if self.__current_temp_after_id is not None:
            self.root.after_cancel(self.__current_temp_after_id)
            self.__current_temp_after_id = None

    def set_temp_for_sec(self, temp, sec):
        self.__cancel_if_temp_after_running()
        self.device.set_temperature(temp)
        self.__current_temp_after_id = self.root.after(sec * 1000,
            lambda *args: self.device.set_temperature(32)
        )

    def destroy(self):
        self.device.set_neutral_temperature()
        # self.add_deferred(start_playback)
        super(self.__class__, self).destroy()
        self.start_playback()

    def start_playback(self):
        manager_class = ManagerThree
        manager_class(
            self.root_path, 'three',
            images=self.__images_to_display_bk,
            images2temps=self.__images2temps
        ).run()
