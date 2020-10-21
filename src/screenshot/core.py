# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
import sys
from datetime import datetime

from aion.logger import lprint, lprint_exception
from aion.microservice import Options, main_decorator
from aion.kanban import KanbanNotFoundError

from .service import ScreenShotService

SERVICE_NAME = "save-screenshot-on-connected-usb-storage"
SAVE_DIRECTORY = "screenshot"


@main_decorator(SERVICE_NAME)
def main(opt: Options):
    conn = opt.get_conn()
    num = opt.get_number()
    lprint("DISPLAY: ", os.environ.get('DISPLAY'))
    
    try:
       while True:
           kanban = conn.get_one_kanban(SERVICE_NAME, num)
           metadata = kanban.get_metadata()
           screen_name = metadata.get('screen_name')
           screenshot_id = metadata.get('screenshot_id')

           if screen_name is None:
               screen_name = "NO_NAME"
           lprint(f"screen_name: {screen_name}")
           lprint(f"screenshot_id : {screenshot_id}")

           timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
           screen = ScreenShotService()

           if screen.check_new_id(screenshot_id):
               screen.shot_and_save(SAVE_DIRECTORY, f"{screen_name}_{timestamp}")
               screen.write_result(screenshot_id)
           else:
               lprint("not new id")

    except KanbanNotFoundError:
            lprint("kanban not found finish")
            sys.exit(0)
    except Exception as e:
            lprint_exception(e)


@main_decorator(SERVICE_NAME)
def main_with_kanban_itr(opt: Options):
    lprint("start main_with_kanban_itri()")
    lprint("DISPLAY: ", os.environ.get('DISPLAY'))
    conn = opt.get_conn()
    num = int(opt.get_number())
    try:
        for kanban in conn.get_kanban_itr(SERVICE_NAME, num):
            metadata = kanban.get_metadata()
            lprint(metadata)
            screen_name = metadata.get('screen_name')
            screenshot_id = metadata.get('screenshot_id')
            if screen_name is None:
                screen_name = "NO_NAME"
            if screenshot_id is None:
                lprint("no screenshot_id")
                continue
            lprint(f"screen_name: {screen_name}")
            lprint(f"screenshot_id : {screenshot_id}")
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            screen = ScreenShotService()
            screen.shot_and_save(SAVE_DIRECTORY, f"{screen_name}_{timestamp}")
            screen.write_result(screenshot_id)
    except Exception as e:
        lprint_exception(e)
    finally:
        pass

