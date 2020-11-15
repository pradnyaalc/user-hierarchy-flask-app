import unittest
import sys

sys.argv = ["Dummy", "config/default_config.properties"]
import EmployeeController

class TestEmployeeController(unittest.TestCase):

    def setUp(self):
        EmployeeController.app.testing = True
        self.app = EmployeeController.app.test_client()

    def test_init(self):
        sys.argv = ["Dummy", "config/default_properties"]
        employees = EmployeeController.init('../input_files/roles.json', '../input_files/employee.json')
        self.assertEqual(len(employees.emp_collection), 5)
        self.assertEqual(len(employees.roles_collection), 5)


