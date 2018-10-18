import os
from .base_manager import BaseManager


class ManagerThree(BaseManager):
    def __init__(self, root_path, name, *args, **kwargs):
        super(self.__class__, self).__init__(root_path, name, *args, **kwargs)
        self.__images_to_display = kwargs['images']
        self.__images2temps = kwargs['images2temps']
        self.__total_images = len(self.__images_to_display)

        self.__root_images_dirname = os.path.join('images', self.name)

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
            self.create_start_view('end_view', info='No images found')
            return

        # view switching
        if prev_view_name != 'end_view':
            # no more starting game
            if len(self.__images_to_display) > 0:
                self.__current_image_fn = image_fn = self.__images_to_display.pop()
                self.__image_object = self.get_image_object(image_fn)
                self.__image_no = self.__total_images - len(self.__images_to_display)
                current_view = self.create_start_view('image_view', layout=1, image_object=self.__image_object, image_no=self.__image_no)

                # temperature
                self.device.set_temperature(
                    self.__images2temps[self.__current_image_fn]
                )
            else:
                current_view = self.create_start_view('end_view', info='Playback complete')
        else:
            # e.g. end view
            self.destroy()

        return current_view

    def interval_reported_4_current_view(self):
        """Override this method in implemented managers to know about time."""
        time_passed = self.current_view.time_spent_until_now()
        if time_passed >= 5.9:
            print 'interval_reported_4_current_view(): Time passed: ', time_passed
            self.root.after(0, lambda: self.current_view.done())
        # time_passed = self.current_view.time_spent_until_now()
        # print 'interval_reported_4_current_view(): Time passed: ', time_passed
