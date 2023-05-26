import json
import tkinter as tk

from queries import Data_analysis,Login_query,Update_services, Employees

from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk

FREE = "Free"
END = "end"
EMPTY = ""
class LoginWindow(tk.Tk):
    royal_blue = "#08147d"
    white = "#ffffff"
    #frozen_white = "#e6f1ff"
    frozen_white = "#ffffff"
    app_title="MOLEYBOLEY"
    def __init__(self):
        super().__init__()
        self.title(self.app_title)
        self.configure(bg=self.frozen_white)
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.load_existing_data()
        self.update_free_employees()
        self.bind("<Configure>", self.on_window_resize)
        self.attributes("-fullscreen", True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_login_frame()

    def on_window_resize(self, event):
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        try:
            self.buttons_width = int(self.screen_width*0.01)
            self.large_font = font.Font(size=25)  

            self.customer_entry.configure(font=self.large_font, width=self.buttons_width)
            self.services_dropdown.configure(font=self.large_font, width=self.buttons_width)
            self.submit_button.configure(font=self.large_font, width=self.buttons_width)
            self.employees_dropdown.configure(font=self.large_font, width=self.buttons_width)
            self.assign_to_button.configure(font=self.large_font, width=self.buttons_width)
            self.employee_entry.configure(font=self.large_font, width=self.buttons_width)
            self.mark_as_free_button.configure(font=self.large_font, width=self.buttons_width)
            self.next_in_line.configure(font=self.large_font,bg=self.white,highlightcolor=self.royal_blue,highlightthickness=2,
                                         width=self.buttons_width,height=3)
            self.next_info.configure(font=self.large_font,bg=self.frozen_white, width=self.buttons_width)



            self.wait_list.tag_configure('large_font', font=self.large_font)
            self.employee_list.tag_configure('large_font', font=self.large_font)

            row_height = self.large_font.metrics("linespace") + 4 
            self.style.configure("Custom.Treeview", rowheight=row_height, font=self.large_font)
            self.style.configure("Custom.Treeview.Heading", font=self.large_font,background=self.royal_blue,foreground=self.white)
        except AttributeError:
            pass
    def grid_all_buttons(self):
        self.customer_entry.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="new")
        self.services_dropdown.grid(row=1, column=0, padx=0, pady=(0, 0), sticky="new")
        self.submit_button.grid(row=2, column=0, padx=0, pady=(0, 7),sticky="new")
        self.next_info.grid(row=3, column=0, padx=0, pady=(0, 0),sticky="new")
        self.next_in_line.grid(row=4, column=0, padx=0, pady=(10, 10),sticky="new")
        self.employees_dropdown.grid(row=5, column=0, padx=0, pady=(10, 0),sticky="new")
        self.assign_to_button.grid(row=6, column=0, padx=0, pady=(0, 23),sticky="new") 
        self.employee_entry.grid(row=7, column=0, padx=0, pady=(0, 0),sticky="new") 
        self.mark_as_free_button.grid(row=8, column=0, padx=0, pady=(0,0),sticky="new")

    def load_existing_data(self):
        with open("data.json", "r") as file:
            data = json.load(file)
            self.services:list = data["services"] 
            self.accounts:dict = data["accounts"]
            self.customers_served:dict = data["customers_served"]
        query = Employees()
        self.employees = query.get_employees()
    
    def create_login_frame(self):
        self.frame = tk.Frame(self, bg=self.royal_blue,padx=50,pady=15, highlightthickness=4, highlightbackground="silver",relief='ridge')
        self.frame.place(relx=0.5, rely=0.5, anchor="center")


        self.username_label = tk.Label(self.frame, text="Username:", bg=self.royal_blue, fg=self.white)
        self.username_label.grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)
        self.username_entry.bind("<Return>",self.login)

        self.password_label = tk.Label(self.frame, text="Password:", bg=self.royal_blue, fg=self.white)
        self.password_label.grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)
        self.password_entry.bind("<Return>",self.login)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = tk.Checkbutton(self.frame, variable=self.show_password_var, 
                                                  command=self.show_password,bg=self.royal_blue,activebackground=self.royal_blue)
        self.show_password_check.grid(row=2, column=1,padx=0,sticky="w")
        self.show_password_var.set(False)

        show_password_label = tk.Label(self.frame, text="Show Password", bg=self.royal_blue, fg=self.white)
        show_password_label.grid(row=2, column=1, sticky="w", padx=(20, 0))

        self.forgot_password_label = tk.Label(self.frame, text="Forgot Password", fg=self.white, bg=self.royal_blue, cursor="hand2")
        self.forgot_password_label.grid(row=3, columnspan=2, pady=10)
        self.forgot_password_label.bind("<Button-1>", self.forgot_password)

        login_button = tk.Button(self.frame, text="Login", command=lambda: self.login(None), bg=self.royal_blue, fg=self.white)
        login_button.grid(row=4, columnspan=2)

    def create_main_frame(self):
        self.create_header_on_main_frame()
        self.create_two_sub_frames()
        self.create_ttk_trees()
        self.create_buttons_frame()
    def create_header_on_main_frame(self):
        self.main_frame = tk.Frame(self, bg=self.frozen_white)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
         

        header = tk.Frame(self.main_frame,bg=self.frozen_white)
        header.grid(row=0, column=0, sticky="n")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.image_header = Image.open("images/business_logo.jpg")   
        self.business_logo =ImageTk.PhotoImage(self.image_header)
        app_label = tk.Label(header, image=self.business_logo)
        app_label.grid(row=0, column=0, padx=10, pady=0)

        header.grid_rowconfigure(0, weight=1)
    
    def create_two_sub_frames(self):
        self.workarea = tk.Frame(self.main_frame, bg=self.frozen_white)
        self.workarea.grid(row=1, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(1, weight=1)
    def create_ttk_trees(self):
        self.trees = tk.Frame(self.workarea, bg=self.frozen_white)
        self.trees.grid(row=0, column=0, sticky="w")

        self.wait_list_frame = tk.Frame(self.trees, borderwidth=1, relief="solid", bg=self.royal_blue)
        self.wait_list_frame.grid(row=0, column=0, sticky="new", pady=(0, 25))

        self.wait_list = ttk.Treeview(self.wait_list_frame, height=int(self.screen_height*0.0095), style="Custom.Treeview")
        self.wait_list.grid(row=0, column=0, pady=0,sticky="new")
        self.wait_list['columns'] = ("Service",)
        self.wait_list.heading("#0", text="Customer Name")
        self.wait_list.heading("Service", text="Service")
        self.wait_list.column("#0", width=int(self.screen_width*.75/2))
        self.wait_list.column("Service", width=int(self.screen_width*.75/2))
        self.wait_list.bind("<Delete>", lambda event: self.delete_item(event=event,isWaitList=True,manual_delete=True))


        self.wait_list_frame = tk.Frame(self.trees, borderwidth=1, relief="solid", bg=self.royal_blue)
        self.wait_list_frame.grid(row=1, column=0, sticky="sew")

        self.employee_list = ttk.Treeview(self.wait_list_frame, height=int(self.screen_height*0.005), style="Custom.Treeview")
        self.employee_list.grid(row=0, column=0, sticky="sew")
        self.employee_list['columns'] = ("Service", "Status")

        self.employee_list.heading("#0", text="Employee Name")
        self.employee_list.heading("Service", text="Service")
        self.employee_list.heading("Status", text="Status")

        self.employee_list.column("#0", width=int(self.screen_width*.75/3))
        self.employee_list.column("Service", width=int(self.screen_width*.75/3))
        self.employee_list.column("Status", width=int(self.screen_width*.75/3))
        self.employee_list.bind("<Delete>", lambda event: self.delete_item(event=event,isWaitList=False,manual_delete=True))
        self.employee_list.bind("<Button-1>",self.on_employee_left_click)
        self.employee_list.bind("<Double-1>",self.on_employee_double_click)
        self.add_initial_items_on_employee_list()

        self.trees.columnconfigure(0, weight=1)
        self.trees.rowconfigure(0, weight=2)
        self.trees.rowconfigure(1, weight=1)

    def on_employee_left_click(self,event):
        self.employee_entry.delete(0,tk.END)
        self.employee_list
        selected_item=self.employee_list.focus()
        employee_name = self.employee_list.item(selected_item)
        self.employee_entry.insert(0, employee_name["text"])
    
    def on_employee_double_click(self,event):
        message = f'The following data only includes those who are added during this session.\n\n'

        for key,value in self.customers_served.items():
            message+=f'{key} = {value} customers\n'
        
        messagebox.showinfo("Employees Served Today",message=message)

    def add_initial_items_on_employee_list(self):
        for employee, values in self.employees.items():
            self.employee_list.insert(EMPTY,tk.END,values=values, iid=employee,text=employee)


    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.workarea, bg=self.frozen_white)
        self.buttons_frame.grid(row=0, column=1, padx=5,sticky="n")
        
        self.customer_entry = ttk.Entry(self.buttons_frame)
        self.customer_entry.insert(0, "Enter customer name")
        self.customer_entry.bind("<FocusIn>", lambda event :self.clear_placeholder(event = event,isCustomer=True))
        self.customer_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event=event,isCustomer=True))

        self.services_dropdown = ttk.Combobox(self.buttons_frame, values=self.services, state="readonly",foreground=self.white, background=self.royal_blue)
        self.submit_button = tk.Button(self.buttons_frame, text="Submit",fg=self.white, bg=self.royal_blue,
                                       command=lambda: self.submit_button_clicked(None))
        self.services_dropdown.bind('<Return>',self.submit_button_clicked)
        
        self.next_info = tk.Label(self.buttons_frame, text="Next in Line: ")
        self.next_in_line = tk.Label(self.buttons_frame)


        self.employee_entry = ttk.Entry(self.buttons_frame)
        self.employee_entry.insert(0, "Add employee name here")
        self.employee_entry.bind("<FocusIn>", lambda event :self.clear_placeholder(event = event,isCustomer=False))
        self.employee_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event=event,isCustomer=False))
        self.employee_entry.bind("<Return>", self.add_employee)
        
          
        self.employees_dropdown = ttk.Combobox(self.buttons_frame, values=self.free_employees, state="readonly",foreground=self.white, background=self.royal_blue)
        self.assign_to_button = tk.Button(self.buttons_frame, text="Assign-to",fg=self.white, bg=self.royal_blue,command=self.assign_customer_to_employee)
        self.mark_as_free_button = tk.Button(self.buttons_frame, text="Mark as Free",fg=self.white, bg=self.royal_blue, command=self.mark_as_free)
        self.grid_all_buttons()

    def update_next_in_line(self):
        try:
            first_item = self.wait_list.item(self.wait_list.get_children()[0])
            next_in_line_text = first_item['text'] 
            self.next_in_line.configure(text=next_in_line_text)
        except IndexError:
            self.next_in_line.configure(text=EMPTY)

    def delete_item(self,event,isWaitList:bool,employee_name=None,manual_delete=False):
        if manual_delete:
            result = messagebox.askyesno("Confirmation", "Are you sure you want to delete this?\n This is IRREVERSIBLE")
            if not result:
                return

        if isWaitList:
            selected_item = self.wait_list.focus()
            if not selected_item:
                name=self.next_in_line.cget("text")
                for item in self.wait_list.get_children():
                    if self.wait_list.item(item,"text")==name:
                        selected_item=item
            if not selected_item:
                return None
            service, =self.wait_list.item(selected_item)['values']
            values = f"{service}: {self.wait_list.item(selected_item)['text']}"
            self.wait_list.delete(selected_item)
            self.update_next_in_line()
            return values
        
        if employee_name is None:
            selected_item = self.employee_list.focus()
            employee_name:str = self.employee_list.item(selected_item)['text']
            self.employee_list.delete(selected_item)
            self.update_next_in_line()            
        deleted_employee=employee_name
        with open("data.json", "r+") as file:
            data = json.load(file)
            data["employees"].pop(employee_name)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        if employee_name is not None:
            for item in self.employee_list.get_children():
                if self.employee_list.item(item, "text") == deleted_employee:
                    self.employee_list.delete(item)
                    self.update_next_in_line()
                    break
            return deleted_employee

    def add_employee(self,event,status: str = FREE,employee_name = None,mark_as_free_name = None):

        if employee_name is None:
            if mark_as_free_name is None:
                employee_name = self.employee_entry.get()
            else: employee_name = mark_as_free_name  
            self.employee_list.insert(EMPTY, END, values=(EMPTY, status),text=employee_name)
        self.employee_entry.delete(0, END)      
        
        with open("data.json", "r+") as file:
            data = json.load(file)
            data["employees"][employee_name] = status
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def clear_placeholder(self, event,isCustomer):
        if isCustomer:
            if self.customer_entry.get() == "Enter customer name":
                self.customer_entry.delete(0, tk.END)
            return
        if self.employee_entry.get() == "Add employee name here":
            self.employee_entry.delete(0,tk.END)
            

    def restore_placeholder(self, event,isCustomer):
        if isCustomer:
            if not self.customer_entry.get():
                self.customer_entry.insert(0, "Enter customer name")
            return
        if not self.employee_entry.get():
            self.employee_entry.insert(0,"Add employee name here")
            
    def assign_customer_to_employee(self):
        assigned_employee = self.employees_dropdown.get()
        if assigned_employee == EMPTY:
            return
        values = self.delete_item(None, True)
        if values is None:
            return  
        query = Employees()
        query.update_employee_status(assigned_employee,service=values)    
        self.update_employee_list(assigned_employee,values,"Busy")
        self.update_employee_dropdown()
        self.update_next_in_line()

    def update_employee_dropdown(self):
        self.employees_dropdown.set(EMPTY)
        values = self.update_free_employees()
        self.employees_dropdown['values'] = values

    def update_employee_list(self, employee, service, status):
        
        self.employee_list.set(employee,"Service",service)
        self.employee_list.set(employee,"Status",status)

    def mark_as_free(self):
        employee = self.employee_list.focus()
        self.update_employee_list(employee,EMPTY,FREE)
        query = Employees()
        query.update_employee_status(employee,FREE)
        self.restore_placeholder(None,False)

    def submit_button_clicked(self,event):
        customer_name = self.customer_entry.get()
        selected_service = self.services_dropdown.get()
        if customer_name ==EMPTY or selected_service==EMPTY:
            return
        self.wait_list.insert(EMPTY, END, values=(selected_service,), text=customer_name)
        self.customer_entry.delete(0, END)
        self.services_dropdown.set(EMPTY)
        self.update_next_in_line()
    def update_free_employees(self):
        query = Employees()
        self.free_employees = query.get_free_employees()
        return self.free_employees
    def show_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show=EMPTY)
        else:
            self.password_entry.config(show="*")

    def forgot_password(self, event):
        messagebox.showinfo("Forgot Password", "Please contact the administrator for assistance.")

    def login(self,event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == EMPTY or password == EMPTY: return
        query=Login_query()
        result = query.login(username,password)

        if result:
            messagebox.showinfo("Login", "Login successful!")
            self.frame.destroy()
            self.create_main_frame()
        else:
            messagebox.showerror("Login", "Invalid username or password!")

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
