
import os

with open(f"/home/{os.environ['USER']}/.display_parameter.txt") as f:
    disp = f.read()
    os.environ['DISPLAY'] = f'{disp.strip()}.0'
    print(os.environ['DISPLAY'])


import pyautogui as gui
from aion.logger import lprint, lprint_exception

from .const import DATABASE
from .db import UsbSql
from .save import get_save_path

class ScreenShotService():

    def __init__(self):
        self.save_path = None
        self.is_success = False

    def shot(self):
        try:
            screenshot = gui.screenshot()
            # NOTE: shot twice to take right screen but reason is unkown
            screenshot = gui.screenshot()
        except Exception as e:
            lprint_exception(e)
            raise RuntimeError("fail to screenshot ==> shot")

        return screenshot

    def shot_and_save(self, path, filename):
        try:
            screenshot = self.shot()
            _path = get_save_path(path)
            if not _path:
                raise RuntimeError("not found usb mountpoint")

            self.save_path = os.path.join(_path, f"{filename}.png")
            screenshot.save(self.save_path)
            lprint(f"save screentshot to {self.save_path}")
            self.is_success = True

        except Exception as e:
            lprint_exception(e)
            self.is_success = False

    def write_result(self, _id):
        is_success = 1 if self.save_is_success else 0
        save_path = self.save_path if self.save_path else ""
        with UsbSql(DATABASE) as db:
            try:
                db.write_screenshot_save_result(_id, save_path, is_success)
                lprint(f"write result to mysql: {_id}, {save_path}")
            except Exception as e:
                lprint_exception(e)
                lprint(f"{e} : fail to write result to mysql")

    def check_new_id(self, _id):
        with UsbSql(DATABASE) as db:
            result = db.check_id(_id)
            if not result.get('path'):
                return True
            else:
                return False

    @property
    def save_is_success(self):
        return self.is_success


if __name__ == "__main__":
    sc = ScreenShotService()
    ret = sc.shot_and_save("tmp", "screen")
    if ret:
        sc.write_result(1)
        print("suceess to save screenshot to usb")
    else:
        sc.write_result(1)
        print("fail to save screenshot to usb")
