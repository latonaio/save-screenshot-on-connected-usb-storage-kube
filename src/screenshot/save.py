import os

from .const import DATABASE
from .db import UsbSql

# exclude for jetson special mount
EXCLUDE_MOUNTPOINT = "README"


def get_mount_point():

    with UsbSql(DATABASE) as sql:
        mountpoint = sql.get_mount_point()

    if not mountpoint:
        return None
    return mountpoint.get('mountpoint')


def get_save_path(path):

    try:
        mount = get_mount_point()
        if not mount:
            raise RuntimeError("not found mount point")
        save_path = os.path.join(mount, path)
        if not os.path.exists(save_path):
           os.makedirs(save_path, exist_ok=True)

        return save_path

    except Exception as e:
        raise RuntimeError(f"{str(e)} : cant save to usb")


if __name__ == "__main__":

    mounts = get_mount_point()
    print("mountpoint are :", mounts)

    path = get_save_path('data')
    print(path)

    with open(os.path.join(path, "test.txt"), "w") as f:
        f.write("this is test text")
