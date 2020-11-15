from flaskext.mysql import MySQL
import SQLQueries as sql_query
import csv


class DatabaseConnectionCRUD:
    session = None
    mysql = None
    connect = None
    configs = None

    def __init__(self, app, configs):
        """
        initialize the mysql db and configurations 
        """
        self.mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = configs.get('MYSQL_DATABASE_USER').data
        app.config['MYSQL_DATABASE_PASSWORD'] = configs.get('MYSQL_DATABASE_PASSWORD').data
        app.config['MYSQL_DATABASE_HOST'] = configs.get('MYSQL_DATABASE_HOST').data
        self.configs = configs
        try:
            self.mysql.init_app(app)
        except:
            raise Exception("Unable to connect to Mysql")

    def get_connection(self):
        """
        Connect to the given Mysql DB and create a session for executing queries
        :return:
        """
        try:
            self.connect = self.mysql.connect()
            self.session = self.connect.cursor()
        except Exception as e:

            raise Exception("Error while creating the cursor for MySQL")
        return self.session

    def create_database(self, db_name):
        """
        Create the database if not exists with the name given the config file
        :param db_name:
        :return:
        """
        try:
            create_query = 'create database if not exists ' + db_name;
            self.session.execute(create_query)

            # use the created database for all the further operations
            use_query = 'use ' + db_name
            self.session.execute(use_query)
        except Exception as e:
            raise Exception("Error while creating the given database")

    def create_table(self):
        """
        create the table for roles and employees
        :return:
        """
        try:
            self.session.execute(sql_query.create_table_roles)
            self.session.execute(sql_query.create_table_employee)
            self.connect.commit()
        except Exception as e:
            raise Exception("Error occurred while creating the tables")

    def get_values(self, reader):
        """
        retrieve values from the given csv files
        :param reader:
        :return:
        """
        i = 0
        val = []
        for row in reader:
            if i > 0:
                if len(row) == 3:
                    r_id = int(row[0])
                    r_name = row[1]
                    if row[2] == 'Null':
                        r_parentid = None
                    else:
                        r_parentid = int(row[2])
                    val.append((r_id, r_name, r_parentid))
                else:
                    r_id = int(row[0])
                    r_name = row[1]
                    r_salary = float(row[2].replace(",", ""))
                    r_role_id = int(row[3])
                    val.append((r_id, r_name, r_salary, r_role_id))
            i += 1
        return val

    def initialize_database(self):
        """
        retrieve data from the roles.csv and employees.csv file and insert into database
        :return:
        """
        self.get_connection()
        self.create_database(self.configs.get('DATABASE_NAME').data)
        self.create_table()

        try:
            # read data from roles.csv and insert into roles table
            with open(self.configs.get('input_file_roles_csv').data, 'r') as file:
                reader = csv.reader(file)
                self.session.executemany(sql_query.insert_rows_roles, self.get_values(reader))
                self.connect.commit()
        except:
            raise Exception("Error occurred while reading the roles csv file and inserting values")

        try:
            # read data from employee.csv and insert into employees table
            with open(self.configs.get('input_file_employee_csv').data, 'r') as file:
                reader = csv.reader(file)
                self.session.executemany(sql_query.insert_rows_employees, self.get_values(reader))
                self.connect.commit()
        except:
            raise Exception("Error occurred while reading the employees csv file and inserting values")
