from collections import deque
from CollectionInterface import Collection
from models import Employee


class EmployeeCollections(Collection):
    emp_collection = dict()

    def __init__(self, roles_collection):
        """
        initialize the employee collection class with roles collection
        As each employee has atleast 1 role associated to him/her
        :param roles_collection: roles dictionary collection
        """
        if len(roles_collection) != 0:
            self.roles_collection = roles_collection
        else:
            raise Exception("To add employees atleast one role should be specified")

    def read_data_and_build_hierarchy(self, collection, schema_path):
        """
        Reads the given employees json and creates a employees dictionary collection
        :param collection: employees data list
        :param schema_path: schema to validate the input data
        :return:
        """
        # validate the given employee json data with the given schema
        if self.validate_collection(collection, schema_path):
            for user in collection:
                user_obj = Employee(user['Id'], user['Name'])
                role_id = user['Role']
                if role_id in self.roles_collection:
                    user_obj.role = self.roles_collection[role_id]
                self.emp_collection[user_obj.id] = user_obj
        else:
            raise Exception("Error in the given json file")

    def get_subordinates(self, employee_id):
        """
        Given the valid employee id return all the subordinate employees
        :param employee_id: integer employee id
        :return: subordinate employee object list
        """
        sub_employees = []
        # check if given employee id exists in employee collection
        if employee_id in self.emp_collection:
            employee = self.emp_collection[employee_id]
            sub_employee_role_id = []
            #retrieve the role hierarchy for the particular employee
            subs = deque(employee.role.subordinates.copy())

            # retrieve all the role ids for the subordinate employees
            while len(subs) > 0:
                sub_employee_role_id.append(subs[0].id)
                if len(subs[0].subordinates) != 0:
                    subs.extend(subs[0].subordinates.copy())
                subs.popleft()

            # retrieve all the subordinate employee based on the role id
            for emp in self.emp_collection.values():
                if emp.role.id in sub_employee_role_id:
                    sub_employees.append(emp)
        else:
            raise Exception("Employee is not present in the json data")

        return sub_employees

    # def get_sub_role(self, role):
    #     subs = role.subordinates
    #     if len(subs) == 0:
    #         return []
    #     for rol in subs:
    #         return [role.id] + self.get_sub_role(rol)


    def get_emp_collection(self):
        return self.emp_collection
