import re
import my_log
from File_Handler import UsersFileHandler


def validation_phone_number(number):
    if len(number) == 11 and number.isdigit():
        return True
    else:
        my_log.logger.info(f"{number} is not a correct phone number!")
        return False


def validation_time(time1):
    regex = r'^\d{2}:\d{2}:\d{2}\s*$'
    if re.search(regex, time1):
        return True


def validation_password(password):
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    if re.search(regex, password):
        return True


def username_exists(username):
    users = UsersFileHandler()
    all_users = users.read_file()
    username_not_found = True
    if all_users:
        for item in all_users:
            if item['username'] == username:
                username_not_found = False
                my_log.logger.info(f"{username} is not a valid and it already exists!")
                return username_not_found
        if username_not_found:
            return True
    return True
