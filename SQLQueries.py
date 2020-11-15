create_table_roles = "create table if not exists roles(" \
                     "id int,name varchar(80)," \
                     "parentid int," \
                     "PRIMARY KEY (id)," \
                     "CONSTRAINT idx_roles_parentid FOREIGN KEY (parentid)" \
                     "REFERENCES roles(id))"

create_table_employee = "create table if not exists employees (" \
                        "id int,name varchar(80)," \
                        "salary numeric(18,2)," \
                        "roleid int," \
                        "Primary key (id)," \
                        "CONSTRAINT fk_role_id FOREIGN KEY (roleid)" \
                        "REFERENCES roles(id))"

insert_rows_roles = "insert ignore into roles(id, name, parentid) values (%s, %s, %s)"

insert_rows_employees = "insert ignore into employees(id, name, salary, roleid) values (%s, %s, %s, %s)"

employee_subordinates = "select e.name as employee_name, r.name as role_name \
                    from employees e, roles r \
                    where e.roleid = r.id \
                    and r.id = %(id)s \
                    and e.name = %(name)s \
                    union \
                    select employee_name, role_name\
                    from (select e.id, e.name as employee_name, e.roleid as roleid, r.name as role_name, r.parentid as parent \
		            from employees e, roles r \
		            where e.roleid = r.id \
		            order by r.parentid, e.roleid) sorted_roles, \
                    (select @pv := %(id)s) initialisation \
                    where   find_in_set(parent, @pv) \
                    and     length(@pv := concat(@pv, ',', roleid))"

role_average_salary = "select r.name as role_name, avg(e.salary) as average_salary \
                                   from employees e, roles r \
                                   where e.roleid = r.id and \
                                   r.id = %(id)s"
all_employees = "select id as employee_id, name as employee_name, roleid as employee_role from employees"
