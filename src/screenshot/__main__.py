# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
from . import main, main_with_kanban_itr

KANBAN_MODE = os.environ.get("KANBAN_MODE", "main")

if __name__ == "__main__":
    if KANBAN_MODE == "main":
        main()
    elif KANBAN_MODE == "main_with_kanban_itr":
        main_with_kanban_itr()
