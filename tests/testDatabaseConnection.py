import unittest
import sys
from jproperties import Properties
from DatabaseConnection import DatabaseConnectionCRUD

sys.argv = ["Dummy", "config/default_config.properties"]
from EmployeeController import app

class TestDatabaseConnection(unittest.TestCase):
    def test_mysql_connection_with_different_config(self):
        configs = Properties()
        with open('config/dummy_config.properties', 'rb') as config_file:
            configs.load(config_file)
        db = DatabaseConnectionCRUD(app, configs)

        with self.assertRaises(Exception) as context:
            db.get_connection()

        self.assertEqual('Error while creating the cursor for MySQL', context.exception.__str__())

    def test_initialise_database_for_incorrect_csv_files(self):
        configs = Properties()
        with open('config/dummy_config_for_csv.properties', 'rb') as config_file:
            configs.load(config_file)
        db = DatabaseConnectionCRUD(app, configs)

        with self.assertRaises(Exception) as context:
            db.initialize_database()

        self.assertEqual('Error occurred while reading the roles csv file and inserting values', context.exception.__str__())



if __name__ == '__main__':
    unittest.main()
