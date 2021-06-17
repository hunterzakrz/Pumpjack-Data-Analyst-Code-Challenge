# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:48:58 2021

@author: hunter
"""
import pandas as pd
import sqlite3

conn = sqlite3.connect('abcCompanyDB.db') 
c = conn.cursor()

            
abcCompany = {'employee_id':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
        'first_name': ['Darius','Tiger','Malik','Ali','Randall',
                             'Josiah','Dante','Wyatt','Quinn','Oliver',
                             'Thane','Walter','Samson','Beck','Lucas',
                             'John','Quinlan','Ivan','Wang','Stone',
                             'Clayton','Cain'],
        'last_name': ['Mufutau','Elliott','Macaulay','Vance','Deacon',
                      'Lee','Mohammad','Kuame','Oliver','Gary',
                      'Phelan','Lester','Dolan','Walker','Marshall',
                      'Nash','Elliott','Dennis','Ronan','Jameson',
                      'Jarrod','Sean'],
        'salary': [3901,5489,5444,8993,9515
                   ,8113,8446,4817,5513,5158,
                   4957,3864,6855,7077,7499,
                   4269,7503,4048,9319,9354,
                   4102,7353],
        'department_id': [1,2,3,4,2,
                          3,3,4,1,2,
                          3,1,2,3,4,
                          2,3,3,4,1,
                          2,3],
        'dept_name': ['Finance','IT','Sales','Marketing','IT',
                      'Sales','Sales','Marketing','Finance','IT',
                      'Sales','Finance','IT','Sales','Marketing',
                      'IT','Sales','Sales','Marketing','Finance',
                      'IT','Sales'],

        'salary_increment':[10,15,17,16,15,17,17,16,10,15,17,10,15,17,16,15,17,17,16,10,15,17]
        }
df = pd.DataFrame(abcCompany, columns = ['employee_id','first_name', 'last_name','salary','dept_name','department_id','salary_increment'])

df.to_csv('flat_data.csv')

dfEmployee= pd.read_csv ('C:\\Users\\hunte\\flat_data.csv')
dfEmployee = dfEmployee.drop( ['Unnamed: 0','dept_name','salary_increment'], axis=1)
dfEmployee

dfDepartment=pd.read_csv ('C:\\Users\\hunte\\flat_data.csv')
dfDepartment = dfDepartment.drop( ['Unnamed: 0','first_name', 'last_name','salary','employee_id'], axis=1)
dfDepartment

c.execute('''CREATE TABLE Department
             (department_id integer PRIMARY KEY,dept_name text,salary_increment integer)''')

c.execute('''CREATE TABLE Employee
             (employee_id integer PRIMARY KEY ,first_name text, last_name text, salary integer,department_id integer,FOREIGN KEY (department_id) REFERENCES DEPARTMENT (department_id))''')

    

dfEmployee.to_sql("Employee", conn, if_exists="replace")
dfDepartment.to_sql("Department", conn, if_exists="replace")
pd.read_sql_query("select * from Department;", conn)




c.execute('''DROP TABLE updated_salaries;''')
c.execute('''CREATE TABLE updated_salaries
             (employee_id integer,salary integer, salary_increment integer,FOREIGN KEY(employee_id) REFERENCES Employee(employee_id),
              FOREIGN KEY(salary) REFERENCES Employee(salary),
              FOREIGN KEY(salary_increment) REFERENCES Department(salary_increment))''')


dfUpdated_Salaries=pd.read_csv ('C:\\Users\\hunte\\flat_data.csv')
dfUpdated_Salaries = dfUpdated_Salaries.drop( ['Unnamed: 0','first_name', 'last_name','department_id','dept_name'], axis=1)
dfUpdated_Salaries
dfUpdated_Salaries.to_sql('updated_salaries', conn, if_exists='replace')

c.execute('''ALTER TABLE updated_salaries
    ADD COLUMN updated_salary real;''')
    
c.execute('''UPDATE updated_salaries SET updated_salary = cast((salary*(1+(.01*salary_increment))) as real);''')

pd.read_sql_query("select * from updated_salaries;", conn)
conn.commit()
conn.close()
