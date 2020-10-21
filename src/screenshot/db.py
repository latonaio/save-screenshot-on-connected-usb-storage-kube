from aion.mysql import BaseMysqlAccess


class UsbSql(BaseMysqlAccess):

    def get_mount_point(self):

        query = """
                SELECT mountpoint
                FROM usbs
                WHERE state = 1;
                """

        return self.get_query(query)

    def write_screenshot_save_result(self, _id, path, is_success):

        query = f"""
                UPDATE screenshots
                SET path='{path}', is_success={is_success}
                WHERE screenshot_id = {_id};
                """
        self.set_query(query)
        self.commit_query()

    def check_id(self, _id):
        query = f"""
                SELECT *
                FROM  screenshots
                WHERE screenshot_id = {_id};
                """
        return self.get_query(query)

if __name__ == "__main__":

    with UsbSql("PeripheralDevice") as db:
        mountpoint = db.get_mount_point()
        print(mountpoint)

    with UsbSql("ScreenShot") as db:
        try:
            db.write_screenshot_save_result("/media/mount/20200602.png", 0)
            print("success to write screenshot result")
        except Exception as e:
            print(e)
            print("fail to write screenshot result")
