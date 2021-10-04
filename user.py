import csv
import pandas as pd
import hashlib
import my_log
import menu


def password_hashing(password):
    hashed_password = hashlib.sha256(password.encode())
    return hashed_password.hexdigest()


class User:
    def __init__(self, username, password, status='Active', login=True, first_name=None, last_name=None, email=None,
                 address=None):
        self.username = username
        self.password = password
        self.status = status
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address

    @staticmethod
    def register(username, password):
        hash_password = password_hashing(password)
        obj_user = User(username, hash_password)
        row_user_info = [
            [obj_user.username, obj_user.password, obj_user.status, obj_user.login]]
        try:
            with open("user.csv", 'a', newline='') as csv_user_info:
                csv_writer = csv.writer(csv_user_info)
                csv_writer.writerows(row_user_info)
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
            my_log.logger.error('File user_information.csv Not Found')
        else:
            print(f"{username.capitalize()} your username and password has been made.")
        sample = pd.read_csv('user.csv')
        sample.index.name = 'user_id'
        sample.to_csv('user_information.csv', index=True)

    @staticmethod
    def logout(username, status, login):
        location = 0
        try:
            df = pd.read_csv("user_information.csv")  # reading the csv file
        except FileNotFoundError:
            print('Error: File user_information.csv Not Found')
        else:
            with open('user_information.csv') as my_file:
                csv_reader = csv.DictReader(my_file)
                for row in csv_reader:
                    if username == row['username']:
                        df.loc[location, 'status'] = status  # locked/unlocked the column 'status' for username
                        df.loc[location, 'login'] = login
                        df.to_csv("user_information.csv", index=False)  # writing into the file
                    location += 1

    @staticmethod
    def login(username):
        count = 0
        success_login = False
        while count <= 3 and not success_login:
            password = input('Please enter your password:')
            hash_password = password_hashing(password)
            try:
                with open("user_information.csv", "r") as csv_user_info:
                    username_finder = csv.reader(csv_user_info)
                    for line in username_finder:
                        if line[1] == username and line[2] == hash_password and line[3] == 'Blocked':
                            print("Your username is Blocked. Only the admin can activate your username. "
                                  "If necessary, send an activation request email to the admin.")
                            User.logout(username, 'Blocked', 'False')
                            menu.print_menu_register_login()
                            success_login = True
                            break
                        elif line[1] == username and line[2] == hash_password and line[3] == 'Active':
                            print(f"{username.capitalize()} You are logged in system. now choose what you want.")
                            if username == 'admin':
                                my_log.logger.info('Admin logged in')
                                print("************ Welcome Admin ***************")
                                menu.check_inventory()
                                menu.main_admin(username)
                            else:
                                print(f"************ Welcome {username.capitalize()} ***************")
                                User.logout(username, 'Active', 'True')
                                menu.main_customer(username)
                            success_login = True
                            break
                    if not success_login:
                        print("Sorry, this username or password does not exist please try again or register.")
                        count += 1
                    if count == 3:
                        if username != 'admin':
                            User.logout(username, 'Blocked', 'False')
                            menu.print_menu_register_login()
                            my_log.logger.error(
                                f'{username} entered the wrong password 3 times, {username} is Blocked.')
                            break
                        else:
                            my_log.logger.error(f'{username} entered the wrong password 3 times.')
                        print("------------------- Note ---------------------------")
                        print("You entered the wrong password 3 times."
                              "You have been locked out please restart to try again.")
                        menu.print_menu_register_login()
                        break
            except FileNotFoundError:
                print('Error: File user_information.csv Not Found')
                my_log.logger.error('File user_information.csv Not Found')
                break
