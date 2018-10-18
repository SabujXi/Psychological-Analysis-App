import time
import csv


class Experiment:
    strftime_fmt = '%Y-%m-%d %H-%M-%S'

    def __init__(self, config, manager, result_dir):
        self.manager = manager
        self.config = config
        self.__result_dir = result_dir
        self.__filename = self.__make_filename()

        self.__row_count = 0
        self.__csvwriter = None
        self.__csv_file = None
        self.__started = False

    @property
    def row_count(self):
        return self.__row_count

    def start(self):
        assert not self.__started
        csv_path = self.manager.get_path(self.__result_dir, self.__make_filename())
        csvfile = open(csv_path, 'wb')
        self.__csv_file = csvfile
        self.__csvwriter = csv.writer(csvfile)
        self.__started = True

    def __make_filename(self):
        return time.strftime(self.strftime_fmt) + '.csv'

    def add_row(self, row):
        assert self.__started
        self.__csvwriter.writerow(row)
        self.__csv_file.flush()
        self.__row_count += 1

    def end(self):
        assert self.__started
        self.__csv_file.close()
        self.__csv_file = None
        self.__csvwriter = None
        self.__started = False
        self.__row_count = 0
