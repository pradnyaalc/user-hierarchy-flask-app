class Role:
    subordinates = None

    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent

    def __str__(self):
        str_dict = dict()
        str_dict['Role Id'] = self.id
        str_dict['Role Name'] = self.name
        return str_dict


class Employee():

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.role = None

    def __str__(self):
        str_dict = dict()
        str_dict['Employee Id'] = self.id
        str_dict['Name'] = self.name
        str_dict['Role'] = self.role.__str__()
        return str(str_dict)