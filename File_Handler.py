import os
import my_log
import csv
import json


class FileHandler:
    def __init__(self, path='shop_managers.json'):
        self.path = path

    def add_to_file(self, new_value):
        if os.path.exists(self.path):
            with open(self.path) as fp:
                list_obj = json.load(fp)
                list_obj[new_value["shop"]] = new_value
        else:
            list_obj = dict()
            list_obj[new_value["shop"]] = new_value
        with open(self.path, 'w') as json_file:
            json.dump(list_obj, json_file, indent=5)

    def update(self, new_value):
        with open(self.path, 'w') as json_file:
            json.dump(new_value, json_file, indent=5)

    def read(self):
        try:
            with open(self.path, 'r') as fp:
                obj = json.load(fp)
                return obj
        except FileNotFoundError as e:
            my_log.logger.exception(f'{e} No such file or directory', exc_info=True)
            return


class CostumerFileHandler:
    def __init__(self, path='costumers.json'):
        self.path = path

    def add_to_file(self, new_value):
        if os.path.exists(self.path):
            with open(self.path) as fp:
                list_obj = json.load(fp)
                list_obj[new_value["username"]] = new_value
        else:
            list_obj = dict()
            list_obj[new_value["username"]] = new_value
        with open(self.path, 'w') as json_file:
            json.dump(list_obj, json_file, indent=4)

    def update(self, new_value):
        with open(self.path, 'w') as json_file:
            json.dump(new_value, json_file, indent=4)

    def read(self):
        with open(self.path, 'r') as fp:
            obj = json.load(fp)
            return obj


class UsersFileHandler:
    def __init__(self, file_path='All_users.txt'):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, 'r') as my_file:
                reader = csv.DictReader(my_file)
                return list(reader)
        except FileNotFoundError:
            return

    def add_to_file(self, new_value):
        fields = []
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()
        with open(self.file_path, 'a') as my_file:

            writer = csv.DictWriter(my_file, fieldnames=fields, lineterminator='\n')
            if my_file.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)

    def clear(self):
        f = open(self.file_path, "w+")
        f.close()
