import unittest
import json
from RolesCollection import RolesCollection
from EmployeeCollection import EmployeeCollections
from models import Employee


class TestEmployeeCollection(unittest.TestCase):

    def build_role(self):
        with open('input_files/roles.json') as f:
            roles = json.load(f)
            roles_collect = RolesCollection()
            roles_collect.read_data_and_build_hierarchy(roles, 'input_files/schema/roles_schema.json')
            roles_collect.get_subordinates(roles_collect.root)
        return roles_collect.get_roles_collection()

    def test_read_data_and_build_hierarchy(self):
        roles_collection = self.build_role()
        with open('input_files/employee.json') as f:
            employees = json.load(f)

        emp_collect = EmployeeCollections(roles_collection)
        emp_collect.read_data_and_build_hierarchy(employees, 'input_files/schema/employees_schema.json')

        emp_ids = list(emp_collect.emp_collection.keys())
        self.assertEqual(emp_ids, [1,2,3,4,5])

    def test_read_data_and_build_hierarchy_for_incorrect_json(self):
        emp_dict = {"Id":1, "Name":'Pradnya', "Roleid":2}
        emp = [emp_dict]

        roles_collection = self.build_role()
        emp_collect = EmployeeCollections(roles_collection)

        with self.assertRaises(Exception) as context:
            emp_collect.read_data_and_build_hierarchy(emp, 'input_files/schema/employees_schema.json')
        self.assertEqual('Error in the given json file', context.exception.__str__())


    def test_read_data_and_build_hierarchy_for_no_initial_roles(self):
        with open('input_files/employee.json') as f:
            employees = json.load(f)

        roles_collection = dict()
        with self.assertRaises(Exception) as context:
            emp_collect = EmployeeCollections(roles_collection)

        self.assertEqual('To add employees atleast one role should be specified', context.exception.__str__())

    def test_get_subordinates(self):
        roles_collection = self.build_role()
        with open('input_files/employee.json') as f:
            employees = json.load(f)

        emp_collect = EmployeeCollections(roles_collection)
        emp_collect.read_data_and_build_hierarchy(employees, 'input_files/schema/employees_schema.json')
        sub_emp = emp_collect.get_subordinates(3)

        expected_sub_ids = [2, 5]
        for emp in sub_emp:
            self.assertIsInstance(emp, Employee)
            self.assertTrue(emp.id in expected_sub_ids)

    def test_get_subordinates_for_random_employee(self):
        roles_collection = self.build_role()
        with open('input_files/employee.json') as f:
            employees = json.load(f)

        emp_collect = EmployeeCollections(roles_collection)
        emp_collect.read_data_and_build_hierarchy(employees, 'input_files/schema/employees_schema.json')

        with self.assertRaises(Exception) as context:
            sub_emp = emp_collect.get_subordinates(10)

        self.assertEqual('Employee is not present in the json data', context.exception.__str__())


if __name__ == '__main__':
    unittest.main()