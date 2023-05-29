import sqlite3
import bcrypt
import pandas as pd

from tkinter import messagebox
from dataclasses import dataclass
from datetime import datetime, timedelta

DATABASE_PATH: str = "data.db"
@dataclass
class Login_query:
    """
The Login_query class provides methods for logging in users, changing passwords, adding users, deleting users, and getting all usernames.

Intended use:

The Login_query class is intended to be used by molleybolley.py where there's a need to authenticate users.

General description:

The Login_query class provides the following methods:

login(username, password): Logs in the user with the specified username and password.
change_password(username, new_password, isAdmin=None): Changes the password for the user with the specified username. If isAdmin is not None, the user will be granted administrator privileges if the password is changed successfully.
add_user(username, password, role): Adds a new user with the specified username, password, and role.
delete_user(username): Deletes the user with the specified username.
get_all_usernames(isAdmin=3): Gets a list of all usernames, where users with a role less than isAdmin are included.
Parameters:

username: The username of the user to log in, change the password for, add, or delete.
password: The password of the user to log in or change the password for.
new_password: The new password for the user to change.
isAdmin: The role of the user to add or delete. If isAdmin is not None, the user will be granted administrator privileges if the user is added or deleted successfully.
Returns:

login(): Returns a tuple of (True, role) if the user was logged in successfully, or (False, None) if the user was not logged in successfully.
change_password(): Returns True if the password was changed successfully, or False if the password was not changed successfully.
add_user(): Returns True if the user was added successfully, or False if the user was not added successfully.
delete_user(): Returns True if the user was deleted successfully, or False if the user was not deleted successfully.
get_all_usernames(): Returns a list of all usernames based on indicated role. 
    """
    DATABASE_PATH: str = DATABASE_PATH
        
    def login(self, username: str, password: str) -> tuple:
        """
        Returns a tuple of (True, role) if the user was logged in successfully, or (False, None) if the user was not logged in successfully.
        """
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            search_username = 'SELECT * FROM user_accounts WHERE username = ?'
            cursor.execute(search_username, (username,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Login", "Invalid username or password!")
                return None            
            hashed_password = row[2]
            if not self._check_password(password, hashed_password):
                messagebox.showerror("Login", "Invalid username or password!")
                return None
            role = row[3]
            return (True,role)

    def _encrypt_pw(self,pw:str):
        key=b'$2b$12$w./mmhOqxj0PLd8gxrTpfe'
        return bcrypt.hashpw(pw,key)
    
    def _check_password(self, password: str, hashed_password: bytes):
        password_bytes = password.encode('utf-8')
        hashed=self._encrypt_pw(password_bytes)
        return hashed == hashed_password
    
    def change_password(self, username, new_password: str, isAdmin=None) -> bool:
        """
        Returns True if the password was changed successfully, or False if the password was not changed successfully
        """
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            new_password_bytes = new_password.encode("utf-8")
            hashed = self._encrypt_pw(new_password_bytes)

            if isAdmin is None:
                update_password = 'UPDATE user_accounts SET password = ? WHERE username = ?'
                parameters = (hashed, username)
            else:
                update_password = 'UPDATE user_accounts SET password = ?, isAdmin = ? WHERE username = ?'
                parameters = (hashed, isAdmin, username)

            try:
                cursor.execute(update_password, parameters)
                messagebox.showinfo("Success!", f"Password was changed successfully for {username}")
                return True
            except Exception as e:
                messagebox.showerror("Error in changing password", e)
                return False

    def add_user(self, username:str, password:str, role:int)-> bool:
        """
        Returns True if the user was added successfully, or False if the user was not added successfully.
        """
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            insert_user = 'INSERT INTO user_accounts (username, password, isAdmin) VALUES (?, ?, ?)'
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), b'$2b$12$w./mmhOqxj0PLd8gxrTpfe')
                cursor.execute(insert_user, (username, hashed_password, role))
                db.commit()
                messagebox.showinfo("Success!",f'{username} added successfully!')
                return True
            except Exception as e:
                messagebox.showerror("Error in adding user",e)
                return False
    
    def delete_user(self, username) -> bool:
        """
        Returns True if the user was deleted successfully, or False if the user was not deleted successfully.
        """
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            delete_user = 'DELETE FROM user_accounts WHERE username = ?'
            try:
                cursor.execute(delete_user, (username,))
                db.commit()
                messagebox.showinfo("Success!",f'{username} deleted successfully!')
                return True
            except Exception as e:
                messagebox.showerror("Error in deleting user",e)
                return False
    
    def get_all_username(self, isAdmin = 3) ->list:
        """
        Returns a list of all usernames based on indicated role. 
        """
        with sqlite3.connect(self.DATABASE_PATH) as db:
            cursor = db.cursor()
            select_all_usernames = f'SELECT username FROM user_accounts WHERE isAdmin < {isAdmin}'

            try:
                cursor.execute(select_all_usernames)
                rows = cursor.fetchall()
                usernames = [row[0] for row in rows]
                return usernames
            except Exception as e:
                messagebox.showerror("Error in getting usernames",e)
                return []

def Create_Entry_For_Today(date):
    """
    The `Create_Entry_For_Today` function creates a new entry in the `daily_services` table for the current day.

    **Intended use:**

    TO ensure that there are data present in the database daily, Also to avoid errors on the graph for current running data

    **General description:**

    The `Create_Entry_For_Today` function does the following:

    1. Checks if an entry already exists for the current day.
    2. If an entry does not exist, it creates a new entry with the following values:
        * `employee_name`: The name of the employee who provided the service.
        * `date`: The date of the service.
        * `manicure`: The number of manicures provided.
        * `pedicure`: The number of pedicures provided.
        * `threading`: The number of threadings provided.
        * `haircut`: The number of haircuts provided.
        * `hairtreatment`: The number of hair treatments provided.
        * `other`: The number of other services provided.
    3. Commits the changes to the database.

    **Parameters:**

    * `date`: The date of the service.

    **Returns:**

    None.
    """
    database_path = DATABASE_PATH
    with sqlite3.connect(database_path) as db:
        cursor = db.cursor()

        cursor.execute("SELECT date FROM daily_services WHERE date = ?", (date,))
        existing_date = cursor.fetchone()

        if existing_date:
            return
        manicure = 0
        pedicure = 0
        threading = 0
        haircut = 0
        hairtreatment = 0
        other = 0
        employee_query = Employees()
        employee_names = employee_query.get_all_employees()

        for employee_name in employee_names:
            cursor.execute("""
                INSERT INTO daily_services (employee_name, date, manicure, pedicure, threading, haircut, hairtreatment, other)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (employee_name, date, manicure, pedicure, threading, haircut, hairtreatment, other))
        db.commit()

class Update_services:
    def __init__(self):
        self.database_path = DATABASE_PATH

    def update_manicure(self, employee_name, date):
        return self._update_column(employee_name, date, 'manicure')

    def update_pedicure(self, employee_name, date):
        return self._update_column(employee_name, date, 'pedicure')

    def update_threading(self, employee_name, date):
        return self._update_column(employee_name, date, 'threading')

    def update_haircut(self, employee_name, date):
        return self._update_column(employee_name, date, 'haircut')

    def update_hairtreatment(self, employee_name, date):
        return self._update_column(employee_name, date, 'hairtreatment')

    def update_other(self, employee_name, date):
        return self._update_column(employee_name, date, 'other')
    
    def update(self, employee_name, date, column_name):
        return self._update_column(employee_name,date,column_name)

    def _update_column(self, employee_name, date, column_name):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            update_query = f"UPDATE daily_services SET {column_name} = {column_name} + 1 WHERE employee_name = ? AND date = ?"
            try:
                cursor.execute(update_query, (employee_name,date))
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
                employees = {}
                for row in rows:
                    employee_name = row[0]
                    manicure = row[1]
                    pedicure = row[2]
                    threading = row[3]
                    haircut = row[4]
                    hairtreatment = row[5]
                    other = row[6]
                    employees[employee_name] = {
                        "Manicure": manicure,
                        "Pedicure": pedicure,
                        "Threading": threading,
                        "Haircut": haircut,
                        "Hairtreatment": hairtreatment,
                        "Other": other
                    }
                
                df = pd.DataFrame.from_dict(employees, orient='index')              
                
                return df
            except Exception as e:
                print(e)
                return {}

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
             
    def get_running_total_per_day(self, date=datetime.today().date()):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = '''SELECT SUM(manicure), SUM(pedicure), SUM(threading), 
                              SUM(haircut), SUM(hairtreatment), SUM(other)
                              FROM daily_services
                              WHERE date = ?'''
            try:
                cursor.execute(select_query, (date,))
                rows = cursor.fetchall()
                running_service_total = {}
                for row in rows:
                    manicure = 0 if row[0] is None else row[0]
                    pedicure = 0 if row[1] is None else row[1]
                    threading = 0 if row[2] is None else row[2]
                    haircut = 0 if row[3] is None else row[3]
                    hairtreatment = 0 if row[4] is None else row[4]
                    other = 0 if row[5] is None else row[5]
                    running_service_total[date] = {
                        "Manicure": manicure,
                        "Pedicure": pedicure,
                        "Threading": threading,
                        "Haircut": haircut,
                        "Hairtreatment": hairtreatment,
                        "Other": other
                    }
                
                df = pd.DataFrame.from_dict(running_service_total, orient='index')              
                
                return df
            except Exception as e:
                print(e)
                return {}

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
                return (True,)
            except Exception as e:
                print("Error exporting data to Excel:", e)
                return (False,str(e))

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
    def get_all_employees(self):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            select_query = 'SELECT employee_name FROM employees'
            try:
                cursor.execute(select_query)
                rows = cursor.fetchall()
                employees = [row[0] for row in rows]
                return employees
            except Exception as e:
                print("Error retrieving all employees:", e)
                return []
    def add_employee(self, employee_name, username):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            insert_query = 'INSERT INTO employees (employee_name, isFree, username) VALUES (?, ?, ?)'
            try:
                cursor.execute(insert_query, (employee_name, "Free", username))
                db.commit()
                print("Employee added successfully.")
            except Exception as e:
                db.rollback()
                print("Error adding employee:", e)

    def delete_employee(self, username):
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            delete_query = 'DELETE FROM employees WHERE username = ?'
            try:
                cursor.execute(delete_query, (username,))
                db.commit()
                messagebox.showinfo("Successful!","Employee deleted successfully.")
            except Exception as e:
                db.rollback()
                messagebox.showinfo("Error deleting employee", e)
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
    pass