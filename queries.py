import sqlite3
import bcrypt
import pandas as pd

from dataclasses import dataclass
from datetime import datetime, timedelta

DATABASE_PATH: str = "data.db"
@dataclass
class Login_query:
    DATABASE_PATH: str = DATABASE_PATH

    def login(self, username: str, password: str):
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            search_username = 'SELECT * FROM user_accounts WHERE username = ?'
            cursor.execute(search_username, (username,))
            row = cursor.fetchone()
            if not row:
                return None
            hashed_password = row[2]
            return self.check_password(password, hashed_password)

    def encrypt_pw(self,pw:str):
        key=b'$2b$12$w./mmhOqxj0PLd8gxrTpfe'
        return bcrypt.hashpw(pw,key)
    
    def check_password(self, password: str, hashed_password: bytes):
        password_bytes = password.encode('utf-8')
        hashed=self.encrypt_pw(password_bytes)
        return hashed == hashed_password
    
    def change_password(self,username,new_password:str):
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            update_password = 'UPDATE user_accounts SET password = ? WHERE username = ?'
            new_password_bytes = new_password.encode("utf-8")
            hashed=self.encrypt_pw(new_password_bytes)
            try:
                cursor.execute(update_password,(hashed,username))
            except Exception as e:
                print(e)
    
    def add_user(self, username:str, password:str):
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            insert_user = 'INSERT INTO user_accounts (username, password) VALUES (?, ?)'
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), b'$2b$12$w./mmhOqxj0PLd8gxrTpfe')
                cursor.execute(insert_user, (username, hashed_password))
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False
    
    def delete_user(self, username):
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            delete_user = 'DELETE FROM user_accounts WHERE username = ?'
            try:
                cursor.execute(delete_user, (username,))
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False
    
    def get_all_username(self):
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            select_all_usernames = 'SELECT username FROM user_accounts'
            try:
                cursor.execute(select_all_usernames)
                rows = cursor.fetchall()
                usernames = [row[0] for row in rows]
                return usernames
            except Exception as e:
                print(e)
                return []

class Update_services:
    def __init__(self):
        self.database_path = DATABASE_PATH

    def update_manicure(self, service_id):
        return self._update_column(service_id, 'manicure')

    def update_pedicure(self, service_id):
        return self._update_column(service_id, 'pedicure')

    def update_threading(self, service_id):
        return self._update_column(service_id, 'threading')

    def update_haircut(self, service_id):
        return self._update_column(service_id, 'haircut')

    def update_hairtreatment(self, service_id):
        return self._update_column(service_id, 'hairtreatment')

    def update_other(self, service_id):
        return self._update_column(service_id, 'other')

    def _update_column(self, service_id, column_name):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            update_query = f"UPDATE daily_services SET {column_name} = {column_name} + 1 WHERE id = ?"
            try:
                cursor.execute(update_query, (service_id,))
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

class Data_analysis:
    def __init__(self):
        self.database_path = DATABASE_PATH
    def get_total_services_per_day(self, date):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = '''SELECT employee_name, SUM(manicure), SUM(pedicure), SUM(threading), 
                              SUM(haircut), SUM(hairtreatment), SUM(other)
                              FROM daily_services
                              WHERE date = ?
                              GROUP BY employee_name'''
            try:
                cursor.execute(select_query, (date,))
                rows = cursor.fetchall()
                return rows
            except Exception as e:
                print(e)
                return []

    def get_total_services_per_week(self, start_date):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = '''SELECT employee_name, SUM(manicure), SUM(pedicure), SUM(threading), 
                              SUM(haircut), SUM(hairtreatment), SUM(other)
                              FROM daily_services
                              WHERE date >= ? AND date < ?
                              GROUP BY employee_name'''
            end_date = start_date + timedelta(days=7)
            try:
                cursor.execute(select_query, (start_date, end_date))
                rows = cursor.fetchall()
                return rows
            except Exception as e:
                print(e)
                return []
             
    def get_running_total_per_day(self, date):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = '''SELECT employee_name, SUM(manicure), SUM(pedicure), SUM(threading), 
                              SUM(haircut), SUM(hairtreatment), SUM(other)
                              FROM daily_services
                              WHERE date = ?
                              GROUP BY employee_name
                              ORDER BY employee_name'''
            try:
                cursor.execute(select_query, (date,))
                rows = cursor.fetchall()
                running_totals = []
                previous_totals = [0] * 6  # Initialize previous totals to zeros for each service
                for row in rows:
                    current_totals = [row[i + 1] + previous_totals[i] for i in range(6)]  # Calculate running totals
                    running_totals.append((row[0], tuple(current_totals)))  # Append employee and running totals
                    previous_totals = current_totals
                return running_totals
            except Exception as e:
                print(e)
                return []

class ExportData:
    def __init__(self):
        self.database_path = DATABASE_PATH

    def export_to_excel(self, output_file, start_date=None, end_date=None):
        with sqlite3.connect(self.database_path) as db:
            select_query = '''SELECT * FROM daily_services'''
            if start_date and end_date:
                select_query += ' WHERE date BETWEEN ? AND ?'
                query_params = (start_date, end_date)
            elif start_date:
                select_query += ' WHERE date >= ?'
                query_params = (start_date,)
            elif end_date:
                select_query += ' WHERE date <= ?'
                query_params = (end_date,)
            else:
                query_params = ()

            try:
                df = pd.read_sql_query(select_query, db, params=query_params)
                df.to_excel(output_file, index=False)
                print(f"Data exported to '{output_file}' successfully.")
            except Exception as e:
                print("Error exporting data to Excel:", e)

class Employees:
    def __init__(self):
        self.database_path = DATABASE_PATH

    def get_employees(self):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = 'SELECT employee_name,service, isFree FROM employees'
            try:
                cursor.execute(select_query)
                rows = cursor.fetchall()
                employees = {}
                for row in rows:
                    employee_name, service, is_free = row
                    employees[employee_name] = (service,is_free)
                return employees
            except Exception as e:
                print("Error retrieving employees:", e)
                return {}


    def add_employee(self, employee_name):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            insert_query = 'INSERT INTO employees (employee_name, isFree) VALUES (?, ?)'
            try:
                cursor.execute(insert_query, (employee_name, "Free"))
                db.commit()
                print("Employee added successfully.")
            except Exception as e:
                db.rollback()
                print("Error adding employee:", e)

    def delete_employee(self, employee_id):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            delete_query = 'DELETE FROM employees WHERE id = ?'
            try:
                cursor.execute(delete_query, (employee_id,))
                db.commit()
                print("Employee deleted successfully.")
            except Exception as e:
                db.rollback()
                print("Error deleting employee:", e)

    def update_employee(self, employee_id, new_name, is_free):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            update_query = 'UPDATE employees SET employee_name = ?, isFree = ? WHERE id = ?'
            try:
                cursor.execute(update_query, (new_name, is_free, employee_id))
                db.commit()
                print("Employee updated successfully.")
            except Exception as e:
                db.rollback()
                print("Error updating employee:", e)

    def update_employee_status(self, employee_name, is_free="Busy", service = ""):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            update_query = 'UPDATE employees SET isFree = ?, service = ? WHERE employee_name = ?'
            try:
                cursor.execute(update_query, (is_free, service, employee_name))
                db.commit()
                print("Employee status updated successfully.")
            except Exception as e:
                db.rollback()
                print("Error updating employee status:", e)

    def get_free_employees(self):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = 'SELECT employee_name FROM employees WHERE isFree = "Free"'
            try:
                cursor.execute(select_query)
                rows = cursor.fetchall()
                employees =[]
                for row in rows:
                    employees.append(row[0])
                return employees
            except Exception as e:
                print("Error retrieving free employees:", e)
                return []

if __name__ == "__main__":
    p = 'password'
    a = Login_query()
    # b= a.login('admin',p)
    # print(b)

    # key=b'$2b$12$w./mmhOqxj0PLd8gxrTpfe'
    # password_bytes = p.encode('utf-8')
    # hashed=bcrypt.hashpw(password_bytes,key)
    # print(hashed)
    # c = bcrypt.checkpw(hashed,b'$2b$12$w./mmhOqxj0PLd8gxrTpfegw6G/wHR30ReEU1pIuF1fpFOF4zwtoq')
    # d = hashed == b'$2b$12$w./mmhOqxj0PLd8gxrTpfegw6G/wHR30ReEU1pIuF1fpFOF4zwtoq'
    # print (c)
    # print (d)

    # e = b'$2b$12$w./mmhOqxj0PLd8gxrTpfegw6G/wHR30ReEU1pIuF1fpFOF4zwtoq'.decode()
    # print(e)
    # u = 'superuser'
    # f = a.change_password(u,"Denver")
    # a.change_password('admin',p)
    # print(f)
    # g = a.login(u,'Denver')
    # print(g)
    # h = a.login('admin',p)
    # print(h)
    # i = a.change_password('megauser',"Password")
    # print(a.login('megauser',"Password"))
    j = a.add_user("Denver","Denver")
    k=a.login('Denver','Denver')
    print(k)