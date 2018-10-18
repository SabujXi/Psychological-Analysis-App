import os
import os.path
from PIL import Image
import csv


class Name2Temperature:
    """
    Name to temperature.
    """
    def __init__(self, config, manager, images_dir, data_dir, data_fn):
        self.manager = manager
        self.config = config
        self.__images_dir = images_dir
        self.__data_dir = data_dir
        self.__data_fn = data_fn
        self.__temp_map = self.__read_data()
        self.__populate_file_abs_paths()

    def get_names(self):
        return self.__temp_map.keys()

    def get_temp(self, fname):
        return self.__temp_map[fname]['temp']

    def get_path(self, fname):
        return self.__temp_map[fname]['path']

    def get_image_data(self, fname):
        path = self.get_path(fname)
        return Image.open(path), path

    def _get_data_fn_abs(self):
        return self.manager.get_path(self.__data_dir, self.__data_fn)

    def __set_path(self, fname, path):
        self.__temp_map[fname]['path'] = path

    def __read_data(self):
        name_temp_map = {}
        csv_path = self._get_data_fn_abs()
        with open(csv_path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            idx = -1
            for row in csvreader:
                idx += 1
                if idx == 0:
                    # skip the first line considering it the header
                    continue
                fn = row[0]
                fn = fn.replace('\\', '/')
                # remove C if exists
                _temp = row[1]
                if _temp.lower().endswith('c'):
                    temp = int(_temp[:-1])
                else:
                    temp = int(_temp)

                name_temp_map[fn] = {"temp": temp, "path": None}
        return name_temp_map

    def __populate_file_abs_paths(self):
        images_dir_abs = self.manager.get_path(self.__images_dir)
        images_sub_dirs = [d for d in os.listdir(images_dir_abs) if os.path.isdir(self.manager.get_path(self.__images_dir, d))]

        for sub_dir in images_sub_dirs:
            base_fns = [fn for fn in os.listdir(self.manager.get_path(self.__images_dir, sub_dir))
                        if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

            base_fns_wo_ext = [self.manager.get_base_fn_wo_ext(fn) for fn in base_fns]
            self.manager.log('base fn s wo ext: ', base_fns_wo_ext)
            # for fn in base_fns:
            #     fn_wo_ext = '.'.join(fn.rsplit('.', 1)[:-1])
            #     base_fns_wo_ext.append(fn_wo_ext)

            # set the abs path
            i = 0
            for base_fn in base_fns:
                self.manager.log('basefn--to--process: ', base_fn)
                base_fn_wo_ext = base_fns_wo_ext[i]
                if base_fn_wo_ext in self.__temp_map:
                    abs_fn = self.manager.get_path(self.__images_dir, sub_dir, base_fn)
                    self.manager.log('base_fn_wo_ext: ', base_fn_wo_ext)
                    self.manager.log('abs_fn: ', abs_fn)
                    self.__set_path(base_fn_wo_ext, abs_fn)
                i += 1

        # check if there is any base_fn_wo_ext in csv that got no real existing file
        for base_fn_wo_ext, temp_path in self.__temp_map.items():
            self.manager.log('base_fn_wo_ext: ', base_fn_wo_ext)

            path = temp_path['path']
            if path is None:
                raise Exception('File `%s` was specified in csv/spreadsheet, but no corresponding image file found'
                                ' inside any sub directory of `%s`' % (base_fn_wo_ext, self.__images_dir))

    def print_temp_stat(self):
        the_map = self.__temp_map
        for fname in the_map.keys():
            self.manager.info(fname + " : ")
            for key in the_map[fname]:
                self.manager.info("  "+key+" : "+str(the_map[fname][key]))
                self.manager.info("\n")


class DataInput:
    def __init__(self, config, manager):
        self.manager = manager
        self.config = config

    def make_name2temp(self, images_dir, data_dir, data_fn):
        return Name2Temperature(self.config, self.manager, images_dir, data_dir, data_fn)

