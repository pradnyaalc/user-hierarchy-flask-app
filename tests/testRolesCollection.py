import unittest
import json
from RolesCollection import RolesCollection
from models import Role

class TestRolesCollection(unittest.TestCase):
    def test_read_data_and_build_hierarchy(self):
        with open('input_files/roles.json') as f:
            roles = json.load(f)

        roles_collect = RolesCollection()
        roles_collect.read_data_and_build_hierarchy(roles, 'input_files/schema/roles_schema.json')

        self.assertIsInstance(roles_collect.root, Role)
        self.assertEqual(roles_collect.root.id, 1)
        self.assertEqual(roles_collect.root.name, 'System Administrator')
        self.assertEqual(roles_collect.root.parent, 0)

    def test_read_data_and_build_hierarchy_for_incorrect_json(self):
        roles_dict = {"Id":1, "Name":'Pradnya', "Parent":0, "Section": "Finanace"}
        roles = [roles_dict]

        roles_collect = RolesCollection()
        with self.assertRaises(Exception) as context:
            roles_collect.read_data_and_build_hierarchy(roles, 'input_files/schema/roles_schema.json')
        self.assertEqual('Error in the given json file', context.exception.__str__())

    def test_get_subordinates(self):
        with open('input_files/roles.json') as f:
            roles = json.load(f)

        roles_collect = RolesCollection()
        roles_collect.read_data_and_build_hierarchy(roles, 'input_files/schema/roles_schema.json')

        roles_collection = roles_collect.get_roles_collection()
        parent = roles_collection[3]

        roles_collect.get_subordinates(parent)
        expected_sub_ids = [4,5]
        for role in parent.subordinates:
            self.assertIsInstance(role, Role)
            self.assertTrue(role.id in expected_sub_ids)

    def test_get_subordinates_for_random_role(self):
        with open('input_files/roles.json') as f:
            roles = json.load(f)

        roles_collect = RolesCollection()
        roles_collect.read_data_and_build_hierarchy(roles, 'input_files/schema/roles_schema.json')

        parent = Role(6, 'Intern', 0)

        with self.assertRaises(Exception) as context:
            roles_collect.get_subordinates(parent)

        self.assertEqual('Parent node does not exists in the given json data', context.exception.__str__())

    def test_get_subordinates_by_id(self):
        with open('input_files/roles.json') as f:
            roles = json.load(f)

        roles_collect = RolesCollection()
        roles_collect.read_data_and_build_hierarchy(roles, 'input_files/schema/roles_schema.json')

        immediate_subordinate = roles_collect.get_subordinate_by_id(2)

        self.assertIsInstance(immediate_subordinate[0], Role)
        self.assertEqual(immediate_subordinate[0].id, 3)
        self.assertEqual(immediate_subordinate[0].name, 'Supervisor')

if __name__ == '__main__':
    unittest.main()