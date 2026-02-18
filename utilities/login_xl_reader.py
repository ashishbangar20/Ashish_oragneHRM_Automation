from utilities.xlUtils import XLUtils


class LoginDataReader:

    @staticmethod
    def get_login_data(file_path, sheet_name):
        rows = XLUtils.get_row_count(file_path, sheet_name)
        data = []

        for row in range(2, rows + 1):
            username = XLUtils.read_data(file_path, sheet_name, row, 1)
            password = XLUtils.read_data(file_path, sheet_name, row, 2)
            expected = XLUtils.read_data(file_path, sheet_name, row, 3)

            data.append((username, password, expected))

        return data
