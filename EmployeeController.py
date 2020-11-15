"""
This application reads data from json and CSV files containing the organization details.
The webservices exposed helps to determine the sub ordinates of given employee
"""
import sys
from flask import *
from jproperties import Properties
from RolesCollection import RolesCollection
from EmployeeCollection import EmployeeCollections
from DatabaseConnection import DatabaseConnectionCRUD
import SQLQueries as sql_query

app = Flask(__name__)

"""
Reads the properties file provided as an argument and 
stores it as the configuration for future use
"""
configs = Properties()
try:
    with open(sys.argv[1], 'rb') as config_file:
        configs.load(config_file)
except Exception as e:
    raise Exception("Properties file is required", e)


def init(role_path, employee_path):
    """
    Read the given input json files for roles and employees and
    creates an employee collection and roles collection using Object oriented programming
    :param role_path: Input filepath for roles.json
    :param employee_path: Input filepath for employees.json
    :return: Object of Employee collection
    """
    try:
        #load the roles json file
        with open(role_path) as f:
            roles = json.load(f)

        #check if jsonarray
        if isinstance(roles, list):
            roles_collect = RolesCollection()
            roles_collect.read_data_and_build_hierarchy(roles, configs.get('schema_path_roles').data)
            roles_collect.get_subordinates(roles_collect.root)
        else:
            raise Exception ("Please provide a valid json array")

    except Exception as e:
        print("Error while reading the roles json file", e)

    try:
        #load the employees json file
        with open(employee_path) as f:
            employees_list = json.load(f)

        if isinstance(employees_list, list):
            employees = EmployeeCollections(roles_collect.get_roles_collection())
            employees.read_data_and_build_hierarchy(employees_list, configs.get('schema_path_employees').data)
            return employees
        else:
            raise Exception ("Please provide a valid json array")
    except Exception as e:
        print("Error while reading the employees json file")

#initialize the roles collection and employee collections
employees = init(configs.get('input_file_roles_json').data, configs.get('input_file_employee_json').data)

#create Database Connection and insert database values
db = DatabaseConnectionCRUD(app, configs)
db.initialize_database()


@app.route('/')
def home():
    """
    Function to render homepage of the application
    :return:
    """
    return render_template("index.html")


@app.route('/view-user', methods=['GET', 'POST'])
def view_user():
    """
    Based on the chosen employee return all the subordinate employees
    :return:
    """
    all_users = employees.get_emp_collection().values()

    #check for post method
    if request.method == 'POST':
        # retrieve user id from the form
        user_id = request.form['user']
        user_name = employees.get_emp_collection()[int(user_id)].name
        sub_employee = employees.get_subordinates(int(user_id))
        # render employees with their subordinates template
        return render_template("view-user-children.html", all_users=all_users, user_name=user_name, user_id=user_id,
                               sub_employee=sub_employee)

    return render_template("view-user.html", all_users=all_users)


@app.route('/view-database-user', methods=['GET', 'POST'])
def view_db_user():
    """
    Based on chosen employee return all the subordinate employees from the database
    and also display the average salary based on the role of the chosen employee
    :return:
    """
    # retrieve all the employees
    db.session.execute(sql_query.all_employees)
    data = db.session.fetchall()

    # check for post request
    if request.method == 'POST':
        # read employee id and employee name from the form
        form_val = request.form['user']
        form_val = eval(form_val)
        role_id = form_val[0]
        user_name = form_val[1]
        # retrieve all the subordinate employees from the database
        sql_query_subordinates = sql_query.employee_subordinates
        db.session.execute(sql_query_subordinates, {"id": role_id, "name": user_name})
        sub_data = db.session.fetchall()

        # retrieve the average salary based on the role of the chosen employee
        sql_query_average_salary = sql_query.role_average_salary
        db.session.execute(sql_query_average_salary, {"id": role_id})
        avg_data = db.session.fetchall()
        return render_template("view-db-users.html", all_users=list(data), sub_data=sub_data, avg_data=avg_data[0])

    return render_template("db-view-template.html", all_users=list(data))


if __name__ == '__main__':
    app.run()
