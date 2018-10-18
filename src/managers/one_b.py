import os
import random
from .base_manager import BaseManager


class ManagerOneB(BaseManager):
    def __init__(self, root_path, name, *args, **kwargs):
        super(self.__class__, self).__init__(root_path, name, *args, **kwargs)
        self.__name_to_temp = None
        self.__image_names_to_display = []
        self.__total_images = 0
        self.__root_images_dirname = os.path.join('images', self.name)

        self.__experiment = self.make_experiment(os.path.join('results', self.name))
        self.__current_image_fn_wo_ext = None

        self.__data = {}
        self._reset_data()

    def _reset_data(self):
        res = {}
        for key in (
                'image_fn_base',
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
        self.__experiment.start()
        headers = ['image_name', 'valence', 'activation', 'control', 'text',
                   'time_on_image', 'time_on_rating', 'time_on_text']
        self.__experiment.add_row(headers)
        super(self.__class__, self).run(*args, **kwargs)

    def __populate_random_images(self):
        data_input = self.make_input_data()
        self.__name_to_temp = name2temp = data_input.make_name2temp(self.__root_images_dirname,
                                                                    'input_data' + os.sep + self.name, 'data.csv')
        image_names = list(name2temp.get_names())
        random.shuffle(image_names)
        self.__image_names_to_display = image_names

        # randomizing files
        self.__total_images = len(self.__image_names_to_display)

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
            if len(self.__image_names_to_display) > 0:
                self.__current_image_fn_wo_ext = image_fn_wo_ext = self.__image_names_to_display.pop()
                image_object = self.get_image_object_abs(self.__name_to_temp.get_path(image_fn_wo_ext))
                image_no = self.__total_images - len(self.__image_names_to_display)
                current_view = self.create_start_view('image_view', layout=2, image_object=image_object, image_no=image_no)
            else:  # end of presentation
                current_view = self.create_start_view('end_view', info='All images displayed')
        elif prev_view_name == 'image_view':
            current_view = self.create_start_view('sam_view', layout=2)
        elif prev_view_name == 'sam_view':
            current_view = self.create_start_view('text_box_view', layout=2)
        else:
            # e.g. end view
            self.destroy()

        # data collection
        if current_view is not None:
            current_view_name = self.get_view_name_by_class(current_view.__class__)

        if prev_view_name != 'start_view':
            if prev_view_name == 'image_view':
                # data
                self.__data['image_fn_base'] = self.get_base_fn_wo_ext(self.__current_image_fn_wo_ext)
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
        if current_view_name in ('text_box_view', 'sam_view'):
            self.device.set_temperature(32)
        else:
            self.device.set_neutral_temperature()
        return current_view
