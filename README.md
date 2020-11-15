# user-hierarchy-flask-app
Web application displays the employees of an organization known as Best Company and their subordinate employees
The application reads the input data in the form of json files and displays an employee hierarchy based on the role of the employee

## Pre-requisites
* Install MySQL version 5.7 from
```
https://dev.mysql.com/downloads/installer/
```
* Create a username and password for the MySQL DB
* Python 3.7

## Steps to run the application
#### 1. Clone the application and enter the directory
```bash
git clone https://github.com/pradnyaalc/user-hierarchy-flask-app.git
cd user-hierarchy-flask-app
```
#### 2. Install all the necessary libraries
```bash
pip install -r requirements.txt
```

#### 3. Input files
The input_files directory consists of the json data for roles and employees as well as schema associated with the json files
The folder also consists of the roles and employees data in the CSV format that are inserted in the MySQL DB. 

#### 4. Configuration files
* The config folder consists of the default_config properties file which is of the form key=value.
* It consists of all the necessary configuration required for the application.
* Update the configuration values for MYSQL username, password, and host.

#### 3. Run the Flask Application with the properties file as the argument
```bash
python EmployeeController.py config/default_config.properties
```

#### 4. Redirect to the Web Application Url
* In Firefox open *http://localhost:5000/*
* Click on Employee Info to retrieve the employees and their subordinates using json data
![Best_Company_Employee](/screenshots/Employee_info.JPG)
* Click on DB Employees to retrieve the employees and their subordinates using MySQL DB
![Best_Company_DB_Employee](/screenshots/db_employee_info.JPG)

#### 5. Running the unit tests
python -m unittest discover -s tests

## Deployments Steps
Will be updated soon






