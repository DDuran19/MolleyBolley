import json
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import datetime

from queries import Data_analysis,Login_query,Update_services, Employees, ExportData,Create_Entry_For_Today

from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FREE = "Free"
END = "end"
EMPTY = ""
NORTHEASTWEST = "new"
ENTER_KEY="<Return>"
LEFT_CLICK = "<Button-1>"
DOUBLE_LEFT_CLICK = "<Double-1>"
TODAY = datetime.datetime.today().date()
WHITE = "#ffffff"
ROYAL_BLUE ="#08147d"

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class LoginWindow(tk.Tk):
    app_title="MOLEYBOLEY"
    image_header = Image.open("images/business_logo.jpg")
    business_logo = None
    app_label = None
    service_data_to_be_updated:dict = {}

    def __init__(self):
        super().__init__()
        self.title(self.app_title)
        self.configure(bg=WHITE)
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
            if self.screen_height > 900:
                self.large_font = font.Font(size=25)
                self.buttons_width = int(self.screen_width*0.01)

            else:
                self.large_font = font.Font(size=18)
                self.buttons_width = int(self.screen_width*0.015)
                
            

            self.customer_entry.configure(font=self.large_font, width=self.buttons_width)
            self.employees_dropdown.configure(font=self.large_font, width=self.buttons_width)
            self.assign_to_button.configure(font=self.large_font, width=self.buttons_width)
            self.mark_as_free_button.configure(font=self.large_font, width=self.buttons_width)
            self.next_in_line.configure(font=self.large_font,bg=WHITE,highlightcolor=ROYAL_BLUE,highlightthickness=2,
                                         width=self.buttons_width,height=3)
            self.next_info.configure(font=self.large_font,bg=WHITE, width=self.buttons_width)

            row_height = self.large_font.metrics("linespace") + 4 
            self.style.configure("Custom.Treeview", rowheight=row_height, font=self.large_font)
            self.style.map("Custom.Treeview.Heading",
                 background=[("active", ROYAL_BLUE),  
                             ("hover", WHITE)])
            self.employee_list.configure(height=5)
            self.style.configure("Custom.Treeview.Heading", font=self.large_font,background=ROYAL_BLUE,foreground=WHITE)
        except AttributeError:
            pass
    def grid_all_buttons(self):
        self.customer_entry.grid(row=0, column=0, padx=0, pady=(0, 0), sticky=NORTHEASTWEST)
        self.next_info.grid(row=3, column=0, padx=0, pady=(0, 0),sticky=NORTHEASTWEST)
        self.next_in_line.grid(row=4, column=0, padx=0, pady=(10, 10),sticky=NORTHEASTWEST)
        self.employees_dropdown.grid(row=5, column=0, padx=0, pady=(10, 0),sticky=NORTHEASTWEST)
        self.assign_to_button.grid(row=6, column=0, padx=0, pady=(0, 23),sticky=NORTHEASTWEST) 
        self.mark_as_free_button.grid(row=8, column=0, padx=0, pady=(0,0),sticky=NORTHEASTWEST)

    def load_existing_data(self):
        Create_Entry_For_Today(TODAY)
        query = Employees()
        self.employees = query.get_employees()
        query = Data_analysis()
        self.customers_served:pd.DataFrame = query.get_running_total_per_day(TODAY) 

    def create_login_frame(self):
        self.frame = tk.Frame(self, bg=ROYAL_BLUE,padx=50,pady=15, highlightthickness=4, highlightbackground="silver",relief='ridge')
        self.frame.place(relx=0.5, rely=0.5, anchor="center")


        self.username_label = tk.Label(self.frame, text="Username:", bg=ROYAL_BLUE, fg=WHITE)
        self.username_label.grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)
        self.username_entry.bind(ENTER_KEY,self.login)

        self.password_label = tk.Label(self.frame, text="Password:", bg=ROYAL_BLUE, fg=WHITE)
        self.password_label.grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)
        self.password_entry.bind(ENTER_KEY,self.login)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = tk.Checkbutton(self.frame, variable=self.show_password_var, 
                                                  command=self.show_password,bg=ROYAL_BLUE,activebackground=ROYAL_BLUE)
        self.show_password_check.grid(row=2, column=1,padx=0,sticky="w")
        self.show_password_var.set(False)

        show_password_label = tk.Label(self.frame, text="Show Password", bg=ROYAL_BLUE, fg=WHITE)
        show_password_label.grid(row=2, column=1, sticky="w", padx=(20, 0))

        self.forgot_password_label = tk.Label(self.frame, text="Forgot Password", fg=WHITE, bg=ROYAL_BLUE, cursor="hand2")
        self.forgot_password_label.grid(row=3, columnspan=2, pady=10)
        self.forgot_password_label.bind(LEFT_CLICK, self.forgot_password)

        login_button = tk.Button(self.frame, text="Login", command=lambda: self.login(None), bg=ROYAL_BLUE, fg=WHITE)
        login_button.grid(row=4, columnspan=2)

    def create_main_frame(self):
        self.create_header_on_main_frame()
        self.create_two_sub_frames()
        self.create_ttk_trees()
        self.create_buttons_frame()
    def create_header_on_main_frame(self):
        self.main_frame = tk.Frame(self, bg=WHITE)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
         

        header = tk.Frame(self.main_frame,bg=WHITE)
        header.grid(row=0, column=0, sticky="n")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.image_header = Image.open("images/business_logo.jpg")   
        self.business_logo =ImageTk.PhotoImage(self.image_header)
        app_label = tk.Label(header, image=self.business_logo)
        app_label.grid(row=0, column=0, padx=10, pady=0)

        header.grid_rowconfigure(0, weight=1)
    
    def create_two_sub_frames(self):
        self.workarea = tk.Frame(self.main_frame, bg=WHITE)
        self.workarea.grid(row=1, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(1, weight=1)
    def create_ttk_trees(self):
        self.trees = tk.Frame(self.workarea, bg=WHITE)
        self.trees.grid(row=0, column=0, sticky="w")

        self.wait_list_frame = tk.Frame(self.trees, borderwidth=1, relief="solid", bg=ROYAL_BLUE)
        self.wait_list_frame.grid(row=0, column=0, sticky=NORTHEASTWEST, pady=(0, 25))

        self.wait_list = ttk.Treeview(self.wait_list_frame, height=int(self.screen_height*0.0095), style="Custom.Treeview")
        self.wait_list.grid(row=0, column=0, pady=0,sticky=NORTHEASTWEST)
        self.wait_list['columns'] = ("Service",)
        self.wait_list.heading("#0", text="Customer Name")
        self.wait_list.heading("Service", text="Services")
        self.wait_list.column("#0", width=int(self.screen_width*.75/2))
        self.wait_list.column("Service", width=int(self.screen_width*.75/2))
        self.wait_list.bind("<Delete>", lambda event: self.delete_customer(event))


        self.wait_list_frame = tk.Frame(self.trees, borderwidth=1, relief="solid", bg=ROYAL_BLUE)
        self.wait_list_frame.grid(row=1, column=0, sticky="sew")

        self.employee_list = ttk.Treeview(self.wait_list_frame, height=int(self.screen_height*0.005), style="Custom.Treeview")
        self.employee_list.grid(row=0, column=0, sticky="sew")
        self.employee_list['columns'] = ("Service", "Status")

        self.employee_list.heading("#0", text="Employee Name")
        self.employee_list.heading("Service", text="Service")
        self.employee_list.heading("Status", text="Status")

        self.employee_list.column("#0", width=int(self.screen_width * 0.75 / 3))
        self.employee_list.column("Service", width=int((self.screen_width * 0.75 * 2 / 3) * 4 / 5))
        self.employee_list.column("Status", width=int((self.screen_width * 0.75 * 2 / 3) * 1 / 5))
        self.employee_list.bind(DOUBLE_LEFT_CLICK,self.on_employee_double_click)
        self.add_initial_items_on_employee_list()

        self.trees.columnconfigure(0, weight=1)
        self.trees.rowconfigure(0, weight=2)
        self.trees.rowconfigure(1, weight=1)
    
    def on_employee_double_click(self,event):
        self.load_existing_data()
        message = self.customers_served
        query = Data_analysis()
        actuals = query.get_total_services_per_day(TODAY)
        GraphResults(self,message,actuals)

    def add_initial_items_on_employee_list(self):
        for employee, values in self.employees.items():
            self.employee_list.insert(EMPTY,tk.END,values=values, iid=employee,text=employee)


    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.workarea, bg=WHITE)
        self.buttons_frame.grid(row=0, column=1, padx=5,sticky="n")
        
        self.customer_entry = ttk.Entry(self.buttons_frame)
        self.customer_entry.insert(0, "Enter customer name")
        self.customer_entry.bind("<FocusIn>", lambda event :self.clear_placeholder(event = event))
        self.customer_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event=event))
        self.customer_entry.bind(ENTER_KEY,lambda event: self.add_customer(event))
        
        self.next_info = tk.Label(self.buttons_frame, text="Next in Line: ")
        self.next_in_line = tk.Label(self.buttons_frame)
          
        self.employees_dropdown = ttk.Combobox(self.buttons_frame, values=self.free_employees, state="readonly",foreground=WHITE, background=ROYAL_BLUE)
        self.assign_to_button = tk.Button(self.buttons_frame, text="Assign-to",fg=WHITE, bg=ROYAL_BLUE,command=self.assign_customer_to_employee)
        self.mark_as_free_button = tk.Button(self.buttons_frame, text="Mark as Free",fg=WHITE, bg=ROYAL_BLUE, command=self.mark_as_free)
        self.grid_all_buttons()

    def update_next_in_line(self):
        try:
            first_item = self.wait_list.item(self.wait_list.get_children()[0])
            next_in_line_text = first_item['text'] 
            self.next_in_line.configure(text=next_in_line_text)
        except IndexError:
            self.next_in_line.configure(text=EMPTY)

    def delete_customer(self,event):
        selected_customer = self.wait_list.focus()
        if not selected_customer:
            name=self.next_in_line.cget("text")
            for item in self.wait_list.get_children():
                if self.wait_list.item(item,"text")==name:
                    selected_customer=item
        if not selected_customer:
            return None
        service, =self.wait_list.item(selected_customer)['values']
        values = f"{service}: {self.wait_list.item(selected_customer)['text']}"
        self.wait_list.delete(selected_customer)
        self.update_next_in_line()
        return values

    def clear_placeholder(self, event):

        if self.customer_entry.get() == "Enter customer name":
            self.customer_entry.delete(0, tk.END)
            return


    def restore_placeholder(self, event):

        if not self.customer_entry.get():
            self.customer_entry.insert(0, "Enter customer name")
        return

            
    def assign_customer_to_employee(self):
        assigned_employee = self.employees_dropdown.get()
        if assigned_employee == EMPTY:
            return
        values = self.delete_customer(None)
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

    def add_customer(self,event):
        customer_name = self.customer_entry.get()
        if customer_name ==EMPTY:
            return
        new_popup = ServicePopup(self,True,self.get_service_data_to_be_updated, customer_name)
        
    def get_service_data_to_be_updated(self, query_data):
        customer_name = self.customer_entry.get()
        self.service_data_to_be_updated:dict = query_data
        services=[]
        for key,value in self.service_data_to_be_updated.items():
            if value:
                services.append(key)
        selected_service = ", ".join(services)
        self.wait_list.insert(EMPTY, END, values=(selected_service,), text=customer_name)
        self.customer_entry.delete(0, END)
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

class GraphResults(tk.Toplevel):
    
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance = cls
            return super().__new__(cls)
        else:
            return cls._instance

    def __init__(self, parent: tk.Tk, data: pd.DataFrame,actuals:pd.DataFrame):
        super().__init__(parent)
        self.title("Running Services for today")
        self.attributes("-topmost", True)
        self.create_bar_graph(data)
        self.create_table(actuals)
        self.create_extract_buttons()
        center_window(self)

    def destroy(self):
        type(self)._instance = None
        super().destroy()
        

    def create_bar_graph(self,data: pd.DataFrame):
        transposed_data = data.transpose()

        self.figure = plt.Figure(figsize=(6, 4))
        self.axes = self.figure.add_subplot(111)

        transposed_data.plot.bar(ax=self.axes,edgecolor='black', color=ROYAL_BLUE)
        self.axes.set_xticklabels(self.axes.get_xticklabels(), rotation=10)

        for rectangle in self.axes.patches:
            x = rectangle.get_x() + rectangle.get_width() / 2
            y = rectangle.get_height() / 2  
            count_value = int(rectangle.get_height())  
            self.axes.text(x, y, count_value, ha='center', va='center',color=WHITE)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)    

    def create_table(self,data:pd.DataFrame):
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        if data.empty:
            data = self.create_default_for_empty_dataframe()
        if self.screen_height > 900:
            my_font = font.Font(size=12)

        else:
            my_font = font.Font(size=8)

        style = ttk.Style()
        style.configure("myCustom.Treeview",foreground="black",font=my_font)
        style.configure("myCustom.Treeview.Heading", background=ROYAL_BLUE, foreground="WHITE",font=my_font)
        style.map("myCustom.Treeview.Heading",
                 background=[("active", ROYAL_BLUE),  
                             ("hover", WHITE)])
        
        self.actual_table = ttk.Treeview(self,style="myCustom.Treeview")
        self.actual_table["columns"] = data.columns.tolist()
        self.actual_table.configure(height=5)
        counter = 0
        for column in data.columns:
            column_name = column
            if counter == 4:
                column_width = 140
            elif counter == 5:
                column_width = 70
            else: 
                column_width = 90        
            self.actual_table.heading(column, text=column_name, anchor=tk.W)
            self.actual_table.column(column, width=column_width, anchor=tk.W)
            counter +=1

        for index, row in data.iterrows():
            row_total = sum(row)
            self.actual_table.insert("", "end", text=f"{index} ({row_total})", values=row.tolist())
        self.actual_table.heading("#0", text="Employee Name (total)", anchor=tk.W)
        self.actual_table.pack(pady=10)
        label = tk.Label(self, text="Click the Extract button to extract the data.")
        label.pack(pady=10)

    def create_extract_buttons(self):
        extract_frame = tk.Frame(self,bg=WHITE)
        extract_frame.pack(pady=10)
        button_style = ttk.Style()
        button_style.configure("Extract.TButton",foreground=WHITE,background=ROYAL_BLUE)
        button_style.map("Extract.TButton",
                 background=[("active", "green"),  
                             ("hover", ROYAL_BLUE)])

        extract_running = ttk.Button(extract_frame, text="Extract Running Today",style="Extract.TButton")
        extract_7days = ttk.Button(extract_frame, text="Extract Last 7 Days",style="Extract.TButton",
                                   command=self.extract_last_seven_days)
        extract_30days = ttk.Button(extract_frame, text="Extract Last 30 Days",style="Extract.TButton",
                                    command=self.extract_last_thirty_days)
        extract_all = ttk.Button(extract_frame, text="Extract all",style="Extract.TButton",
                                 command=self.extract_all)
        extract_running.grid(row=0, column=0, padx = 5,sticky=NORTHEASTWEST)
        extract_7days.grid(row=0, column=1, padx = 5,sticky=NORTHEASTWEST)
        extract_30days.grid(row=0, column=2, padx = 5,sticky=NORTHEASTWEST)
        extract_all.grid(row=0,column=3, padx = 5,sticky=NORTHEASTWEST)

    def extract_running(self):
        self.toggle_topmost()
        query = ExportData()
        default_file_name = f'Running_data_for_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath,start_date=TODAY)
        self.info_on_result(result)
        self.toggle_topmost()


    def extract_last_seven_days(self):
        self.toggle_topmost()
        query = ExportData()
        seven_days_ago = TODAY - datetime.timedelta(days=7)
        default_file_name = f'Data_from_{seven_days_ago}_until_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath,seven_days_ago,TODAY)
        self.info_on_result(result)
        self.toggle_topmost()

    def extract_last_thirty_days(self):
        self.toggle_topmost()
        query = ExportData()
        thirty_days_ago = TODAY - datetime.timedelta(days=30)
        default_file_name = f'Data_from_{thirty_days_ago}_until_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath,thirty_days_ago,TODAY)
        self.info_on_result(result)
        self.toggle_topmost()

    def extract_all(self):
        self.toggle_topmost()
        query = ExportData()
        default_file_name = f'All_data_Extracted_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath)
        self.info_on_result(result)
        self.toggle_topmost()

    
    def ask_where_to_save(self,default_file_name):
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_file_name)
        return file_path

    def info_on_result(self, result):
        if result[0]:
            messagebox.showinfo("Successful!","Data exported successfully!")
        else:
            messagebox.showinfo("Failed",f"Something went wrong: {result[1]}")
        
    def toggle_topmost(self):
        if self.attributes("-topmost"):
            self.attributes("-topmost", False)
        else:
            self.attributes("-topmost", True)

class ServicePopup(tk.Toplevel):
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance = cls
            return super().__new__(cls)
        else:
            return cls._instance

    def __init__(self, parent: tk.Tk,isCustomer:bool,get_value_from_popup,name,manicure:int=0, pedicure: int = 0,
                 threading:int = 0,haircut: int = 0, hairtreatment:int = 0, other:int = 0):
        super().__init__(parent)
        self.get_value_from_popup=get_value_from_popup
        self.attributes("-topmost", True)
        if isCustomer:
            self.title(f"New Customer - {name}")
        else: self.title(f"Services completed - {name}")
        self.geometry("450x200")
        self.configure(background=WHITE)
        self.manicure = manicure
        self.pedicure  = pedicure
        self.threading  = threading
        self.haircut  = haircut 
        self.hairtreatment  = hairtreatment 
        self.other  = other
        self.setup_frame()
        center_window(self)

    def destroy(self):
        type(self)._instance = None
        super().destroy()
    
    def setup_frame(self):
        frame = tk.Frame(self)
        frame.pack()

        attributes = ["Manicure", "Pedicure", "Threading", "Haircut", "HairTreatment", "Other"]
        checkboxes = []

        # Create checkboxes for attributes
        for i, attribute in enumerate(attributes):
            checkbox = tk.Checkbutton(frame, text=attribute, command=lambda attr=attribute: self.update_attribute(attr))
            checkboxes.append(checkbox)

            # Determine grid position based on row and column
            row = i // 3
            col = i % 3

            checkbox.grid(row=row, column=col, padx=10, pady=5)

        # Set the checkbox values based on the initial attribute values
        checkboxes[0].select() if self.manicure == 1 else checkboxes[0].deselect()
        checkboxes[1].select() if self.pedicure == 1 else checkboxes[1].deselect()
        checkboxes[2].select() if self.threading == 1 else checkboxes[2].deselect()
        checkboxes[3].select() if self.haircut == 1 else checkboxes[3].deselect()
        checkboxes[4].select() if self.hairtreatment == 1 else checkboxes[4].deselect()
        checkboxes[5].select() if self.other == 1 else checkboxes[5].deselect()

        # Create the Submit button
        submit_button = tk.Button(self, text="Submit", command=self.on_submit, bg="#08147d", fg="white")
        submit_button.pack(pady=10)

    def update_attribute(self, attribute):
        checkbox_value = 1 if getattr(self, attribute.lower()) == 0 else 0
        setattr(self, attribute.lower(), checkbox_value)

    def on_submit(self):
        # Create a dictionary to store the checkbox values
        self.checkbox_values = {
            "manicure": self.manicure,
            "pedicure": self.pedicure,
            "threading": self.threading,
            "haircut": self.haircut,
            "hairtreatment": self.hairtreatment,
            "other": self.other
        }
        if sum(self.checkbox_values.values()):
            self.get_value_from_popup(self.checkbox_values)
        self.destroy()

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
    # data = pd.DataFrame({'Category': ['A', 'B', 'C', 'D'],
    #                  'Value': [10, 20, 15, 25]})

    # root = tk.Tk()
    # graph_results = GraphResults(root, data)
    # root.mainloop()
