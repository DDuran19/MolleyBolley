import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import datetime, os.path

from queries import Data_analysis,Login_query,Update_services, Employees, ExportData,Create_Entry_For_Today

from tkinter import Misc, filedialog
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
READONLY = "readonly"

def center_window(window):
    """
    center_window() centers the given window on the screen.

    Args:
        window: The window to be centered.

    Returns:
        None.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def toggle_topmost(window):
    """
    toggle_topmost() toggles the topmost property of the given window.
       topmost means it will always be visible on top of other apps

    Args:
        window: The window whose topmost property is to be toggled.

    Returns:
        None.
    """
    if window.attributes("-topmost"):
        window.attributes("-topmost", False)
    else:
        window.attributes("-topmost", True)

class LoginWindow(tk.Tk):
    """
    LoginWindow() is a class that represents a login window.

    Intended Use:
        To create an Graphic User Interface for viewing the login part and as well as the main workarea comprising of the two tables, customers in queue and employees

    Attributes:
        app_title: The title of the login window.
        image_header: used to store the image so it wont be garbage collected
        business_logo: used to store the image so it wont be garbage collected
        app_label: used to store the image so it wont be garbage collected
        service_data_to_be_updated: The service data to be updated.
        isAdmin: The isAdmin flag of the login window.

    Methods:
        __init__(): The constructor of the LoginWindow class.
        on_window_resize(): The method that is called when the login window is resized.
        grid_all_buttons(): The method that grids all the buttons of the login window.
        load_existing_data(): The method that loads the existing data into the login window.
        create_login_frame(): The method that creates the login frame of the login window.
        create_main_frame(): The method that creates the main frame of the login window.
        create_header_on_main_frame(): The method that creates the header on the main frame of the login window.
        show_admin_panel(): The method that shows the admin panel.
        create_two_sub_frames(): The method that creates the two sub frames of the main frame.
        create_ttk_trees(): The method that creates the ttk trees of the main frame.
        create_buttons_frame(): The method that creates the buttons frame of the main frame.
        on_employee_double_click(): The method that is called when an employee is double clicked in the employee tree.
        add_initial_items_on_employee_list(): The method that adds initial items to the employee tree.
        create_buttons_frame(): The method that creates the buttons frame of the main frame.
    """
    app_title="MOLEYBOLEY"
    image_header = Image.open("images/business_logo.jpg")
    business_logo = None
    app_label = None
    service_data_to_be_updated:dict = {}
    isAdmin = 0

    def __init__(self):
        super().__init__()
        self.title(self.app_title)
        self.configure(bg=WHITE)
        self.customers = Customers()
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

        self.image_header = Image.open("images/business_logo.jpg")   
        max_height = int(self.screen_height * 0.25)
        width, height = self.image_header.size
        aspect_ratio = width / height
        resized_height = min(height, max_height)
        resized_width = int(resized_height * aspect_ratio)
        self.image_header = self.image_header.resize((resized_width, resized_height), Image.ANTIALIAS)
        self.business_logo =ImageTk.PhotoImage(self.image_header)

        header = tk.Frame(self.main_frame,bg=WHITE)
        header.grid(row=0, column=0, sticky="n")
        self.main_frame.grid_columnconfigure(0, weight=1)


        app_label = tk.Label(header, image=self.business_logo)
        app_label.grid(row=0, column=0, padx=10, pady=0)
        app_label.bind(LEFT_CLICK, self.show_admin_panel)
        header.grid_rowconfigure(0, weight=1)
    def show_admin_panel(self,_):
        AdminPanel(self,self.isAdmin,self.username)
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
        self.wait_list.heading("#0", text="Waiting list")
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
        self.buttons_frame.grid(row=0, column=1, padx=5,pady=0, sticky="n")
        
        self.customer_entry = ttk.Entry(self.buttons_frame)
        self.customer_entry.insert(0, "Enter customer name")
        self.customer_entry.bind("<FocusIn>", lambda event :self.clear_placeholder(event = event))
        self.customer_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event=event))
        self.customer_entry.bind(ENTER_KEY,lambda event: self.add_customer(event))
        
        self.next_info = tk.Label(self.buttons_frame, text="Next in Line: ")
        self.next_in_line = tk.Label(self.buttons_frame)
          
        self.employees_dropdown = ttk.Combobox(self.buttons_frame, values=self.free_employees, state=READONLY,foreground=WHITE, background=ROYAL_BLUE)
        self.assign_to_button = tk.Button(self.buttons_frame, text="Assign-to",fg=WHITE, bg=ROYAL_BLUE,command=self.assign_customer_to_employee)
        self.mark_as_free_button = tk.Button(self.buttons_frame, text="Mark as Free",fg=WHITE, bg=ROYAL_BLUE, command=self.mark_as_free)
        self.grid_all_buttons()
        self.insert_survey_and_facebook()

    def insert_survey_and_facebook(self):
        self.socials_frame = tk.Frame(self.buttons_frame, bg="white")
        self.socials_frame.grid(row=10, column=0, padx=5, sticky="s")

        # Add survey logo
        self.survey_logo = Image.open("images/survey.png")
        icon_width = int(self.screen_width * 0.13)
        self.survey_logo = self.survey_logo.resize((icon_width, icon_width)) 
        self.converted_survey_logo = ImageTk.PhotoImage(self.survey_logo)
        self.survey_label = tk.Label(self.socials_frame, image=self.converted_survey_logo, bg="white")
        self.survey_label.pack()
        # Add Facebook logo and text
        self.facebook_logo = Image.open("images/facebook_icon.png")
        self.facebook_logo = self.facebook_logo.resize((40, 40)) 
        self.converted_facebook_logo = ImageTk.PhotoImage(self.facebook_logo)
        self.facebook_label = tk.Label(self.socials_frame, image=self.converted_facebook_logo, bg="white")
        self.facebook_label.pack(side="left")

        facebook_text = "fb.com/MoleyBoley2000"
        self.facebook_text_label = tk.Label(self.socials_frame, text=facebook_text, bg="white",font=self.large_font)
        self.facebook_text_label.pack(side="left")
    def update_next_in_line(self):
        try:
            first_item = self.wait_list.item(self.wait_list.get_children()[0])
            next_in_line_text = first_item['text'].split(". ")[-1] 
            self.next_in_line.configure(text=next_in_line_text)
            self.modify_treeview_values(self.wait_list)

        except IndexError:
            self.next_in_line.configure(text=EMPTY)
    def modify_treeview_values(self,treeview: ttk.Treeview):
        counter = 1
        for index, item_id in enumerate(treeview.get_children(), start=1):
            current_values = treeview.item(item_id)['values']
            current_text = treeview.item(item_id)['text']
            if ". " in current_text:
                current_text=current_text.split(". ")[-1]

            modified_text = f'{counter:02}. {current_text}'
            treeview.delete(item_id)
            treeview.insert('', index-1, text=modified_text, values=current_values)
            counter += 1


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
        values = f'{service}: {self.wait_list.item(selected_customer)["text"].split(". ")[-1]}'
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
        services_by_customer = self.employee_list.item(employee)['values']
        services = ["manicure", "pedicure",
                    "threading", "haircut",
                    "hairtreatment", "other"]
        service_dict = {}
        for service in services:
            if service in services_by_customer[0]:
                service_dict[service]=1

        new = ServicePopup(self,False,self.gather_services_completed_by_employee,
                               employee,**service_dict)
        
        
    def gather_services_completed_by_employee(self):
        employee = self.employee_list.focus()
        self.update_employee_list(employee,EMPTY,FREE)
        query = Employees()
        query.update_employee_status(employee,FREE)
        self.update_employee_dropdown()

    def add_customer(self,event):
        customer_name = self.customer_entry.get()
        if customer_name ==EMPTY:
            return
        new_popup = ServicePopup(self,True,self.get_service_data_to_be_updated, customer_name)
        
    def get_service_data_to_be_updated(self, query_data):
        self.customers.update()
        customer_name = f'     \u2023{self.customers.get():03} {self.customer_entry.get()}'

        # customer_name = f'{self.customers.get():03} \u2192 {self.customer_entry.get()}'
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
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        if self.username == EMPTY or password == EMPTY: return
        query=Login_query()
        result = query.login(self.username,password)
        if result is None:
            return
        if not result[0]:
            return
        messagebox.showinfo("Login", f"Login successful!\n Welcome Back {self.username}")
        self.frame.destroy()
        self.create_main_frame()
        self.isAdmin=result[1]
            
class Customers:
    def __init__(self):
        self.create_file()

    def create_file(self):
        if not os.path.isfile("customers.txt"):
            self.reset()
        else:
            self.get()

    def get(self):
        try:
            with open("customers.txt", "r") as file:
                self.file = int(file.read())
                return self.file
        except ValueError:
            return 0

    def update(self):
        self.file = self.get() + 1
        with open("customers.txt", "w") as file:
            file.write(str(self.file))
        return self.file

    def reset(self):
        self.file = 0
        with open("customers.txt", "w") as file:
            file.write(str(self.file))
        return self.file

class GraphResults(tk.Toplevel):
    """
    This class creates a window that displays a bar graph and a table of data.

    The data can be passed to the constructor as a Pandas DataFrame.

    The window has four buttons:

    * Extract Running Today: Extracts the data for the current day and saves it to an Excel file.
    * Extract Last 7 Days: Extracts the data for the last 7 days and saves it to an Excel file.
    * Extract Last 30 Days: Extracts the data for the last 30 days and saves it to an Excel file.
    * Extract All: Extracts all of the data and saves it to an Excel file.
    
    Intended use:

    The GraphResults class can be used to display a bar graph and a table of data. The data can be passed to the constructor as a Pandas DataFrame. The window has four buttons that allow the user to extract the data for the current day, the last 7 days, the last 30 days, or all of the data. The extracted data is saved to an Excel file.

    General description

    The GraphResults class inherits from the tk.Toplevel class. It has four methods:

    __init__(): This method initializes the window and creates the bar graph and the table of data.
    create_bar_graph(): This method creates the bar graph.
    create_table(): This method creates the table of data.
    create_extract_buttons(): This method creates the four buttons.
    The GraphResults class also has four helper methods:

    extract_running(): This method extracts the data for the current day and saves it to an Excel file.
    extract_last_seven_days(): This method extracts the data for the last 7 days and saves it to an Excel file.
    extract_last_thirty_days(): This method extracts the data for the last 30 days and saves it to an Excel file.
    extract_all(): This method extracts all of the data and saves it to an Excel file.
    """
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
        toggle_topmost(self)
        query = ExportData()
        default_file_name = f'Running_data_for_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath,start_date=TODAY)
        self.info_on_result(result)
        toggle_topmost(self)


    def extract_last_seven_days(self):
        toggle_topmost(self)
        query = ExportData()
        seven_days_ago = TODAY - datetime.timedelta(days=7)
        default_file_name = f'Data_from_{seven_days_ago}_until_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath,seven_days_ago,TODAY)
        self.info_on_result(result)
        toggle_topmost(self)

    def extract_last_thirty_days(self):
        toggle_topmost(self)
        query = ExportData()
        thirty_days_ago = TODAY - datetime.timedelta(days=30)
        default_file_name = f'Data_from_{thirty_days_ago}_until_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath,thirty_days_ago,TODAY)
        self.info_on_result(result)
        toggle_topmost(self)

    def extract_all(self):
        toggle_topmost(self)
        query = ExportData()
        default_file_name = f'All_data_Extracted_{TODAY}.xlsx'
        filepath = self.ask_where_to_save(default_file_name)
        result = query.export_to_excel(filepath)
        self.info_on_result(result)
        toggle_topmost(self)

    
    def ask_where_to_save(self,default_file_name):
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_file_name)
        return file_path

    def info_on_result(self, result):
        if result[0]:
            messagebox.showinfo("Successful!","Data exported successfully!")
        else:
            messagebox.showinfo("Failed",f"Something went wrong: {result[1]}")
        

class ServicePopup(tk.Toplevel):
    """
    This class creates a window that allows a user to select service requested by customer or done by an employee.

    The window has the following widgets:

    A checkbox for each service.
    A button to submit the selected services.

    Intended use:

    The ServicePopup class can be used by users to select services. The window allows users to select one or more services and then submit the selected services.

    General description:

    The ServicePopup class inherits from the tk.Toplevel class. It has the following methods:

    __init__(): This method initializes the window and creates the widgets.
    setup_frame(): This method creates the frame that contains the checkboxes.
    update_attribute(): This method updates the value of the attribute corresponding to the selected checkbox.
    on_submit(): This method submits the selected services.

    """
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
        self.isCustomer = isCustomer
        self.name = name
        if isCustomer:
            self.title(f"New Customer - {name}")
        else: self.title(f"Services completed - {name}")
        self.geometry("400x280")
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
        frame = tk.Frame(self, background=WHITE, bg = WHITE)
        frame.pack()

        attributes = ["Manicure", "Pedicure", "Threading", "Haircut", "HairTreatment", "Other"]
        checkboxes = []

        # Create checkboxes for attributes
        for i, attribute in enumerate(attributes):
            checkbox = tk.Checkbutton(frame, text=attribute, command=lambda attr=attribute: self.update_attribute(attr), 
                                      font=font.Font(size=20), height=2,background=WHITE)
            checkboxes.append(checkbox)

            row = i // 2
            col = i % 2

            checkbox.grid(row=row, column=col, padx=5, pady=0, sticky="w")

        checkboxes[0].select() if self.manicure == 1 else checkboxes[0].deselect()
        checkboxes[1].select() if self.pedicure == 1 else checkboxes[1].deselect()
        checkboxes[2].select() if self.threading == 1 else checkboxes[2].deselect()
        checkboxes[3].select() if self.haircut == 1 else checkboxes[3].deselect()
        checkboxes[4].select() if self.hairtreatment == 1 else checkboxes[4].deselect()
        checkboxes[5].select() if self.other == 1 else checkboxes[5].deselect()

        # Create the Submit button
        submit_button = tk.Button(self, text="Submit", command=self.on_submit, bg="#08147d", fg="white", height=2, width=20)
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
        if self.isCustomer:
            if sum(self.checkbox_values.values()):
                self.get_value_from_popup(self.checkbox_values)
        else: 
            query = Update_services()
            for service_name, value in self.checkbox_values.items():
                if value == 1:
                    query.update(self.name,TODAY,service_name)
            self.get_value_from_popup()
        self.destroy()


class AdminPanel(tk.Toplevel):
    """
    This class creates a window that allows an administrator to manage users and their passwords.

    The window has the following widgets:

    * A dropdown menu that lists all of the users.
    * A text field for the new user's name.
    * A text field for the new user's username.
    * A text field for the new user's password.
    * A checkbox that allows the user to specify whether the new user should be an administrator.
    * A button that creates the new user.
    * A button that deletes the selected user.
    * A button that changes the password of the selected user.
    
    Intended use:

    The AdminPanel class can be used by administrators to manage users and their passwords. The window allows administrators to create new users, delete existing users, and change the passwords of existing users.

    General description

    The AdminPanel class inherits from the tk.Toplevel class. It has the following methods:

    __init__(): This method initializes the window and creates the widgets.
    create_widgets(): This method creates the widgets.
    set_admin_privileges(): This method sets the admin privileges of the selected user.
    passwords_match(): This method checks if the two passwords entered by the user match.
    create_new_employee(): This method creates a new user.
    delete_employee(): This method deletes the selected user.
    change_password(): This method changes the password of the selected user.
    exit_app(): This method closes the window.
    """

    _instance = None
    button_style = {"foreground": WHITE, "background": ROYAL_BLUE, "width":20}

    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance = cls
            return super().__new__(cls)
        else:
            return cls._instance
    def __init__(self, parent:tk.Tk, isAdmin:int, username:str):
        super().__init__(parent)
        self.title(f"Settings Panel - {'Admin' if isAdmin else 'Normal'} mode")
        self.attributes("-topmost", True)
        self.isAdmin:int = isAdmin
        self.username = username
        self.geometry(f"{'850x400' if isAdmin else '400x350'}")
        self.configure(background=WHITE)
        self.get_usernames()
        center_window(self)
        self.create_widgets()
        

    def get_usernames(self):
        query = Login_query()
        
        self.usernames = query.get_all_username(self.isAdmin)
        self.usernames.append(self.username)
    def destroy(self):
            type(self)._instance = None
            super().destroy()

    def create_widgets(self):
        font_style = ("TkDefaultFont", 20)
        self.Entry_style={"font":font_style, "width":20, "background": WHITE}
        main = tk.Frame(self,background=WHITE)
        main.grid(row=0,column=0,padx=10)

        if self.isAdmin:
            self.username_var = tk.StringVar()
            username_dropdown = ttk.Combobox(main, values = self.usernames, textvariable=self.username_var,state=READONLY,font=font_style, width=20)
            username_dropdown.grid(row=0, column=0, pady=10)
            default_value = self.username
            username_dropdown.set(default_value)

            self.adminmode = tk.Frame(self,background=WHITE)
            self.adminmode.grid(row=0, column=1,sticky=NORTHEASTWEST,padx=10)
            create_new_employee_label = tk.Label(self.adminmode, text="Create New Employee", **self.Entry_style)
            create_new_employee_label.grid(row=0, column=0, columnspan=2)

            employee_namelabel = tk.Label(self.adminmode, text="Write new employee name:",background=WHITE)
            employee_namelabel.grid(row=1, column=0, sticky=tk.E)
            self.employee_name = tk.Entry(self.adminmode, **self.Entry_style)
            self.employee_name.grid(row=1, column=1)

            username_label = tk.Label(self.adminmode, text="Username:",background=WHITE)
            username_label.grid(row=2, column=0, sticky=tk.E)
            self.usernameEntry = tk.Entry(self.adminmode, **self.Entry_style)
            self.usernameEntry.grid(row=2, column=1)

            password1_label = tk.Label(self.adminmode, text="Password:",background=WHITE)
            password1_label.grid(row=3, column=0, sticky=tk.E)
            self.password1 = tk.Entry(self.adminmode, show="*", **self.Entry_style)
            self.password1.grid(row=3, column=1)

            password2_label = tk.Label(self.adminmode, text="Confirm Password:",background=WHITE)
            password2_label.grid(row=4, column=0, sticky=tk.E)
            self.password2 = tk.Entry(self.adminmode, show="*", **self.Entry_style)
            self.password2.grid(row=4, column=1)

            self.role_checkbox_var = tk.BooleanVar()

            role_checkbox = tk.Checkbutton(self.adminmode, text="Add admin privileges?", background=WHITE,
                               variable=self.role_checkbox_var, command=self.set_admin_privileges)
            role_checkbox.grid(row=5, column=1, sticky=tk.W)


            create_employee_button = tk.Button(self.adminmode, text="Create New Employee", **self.button_style,command=self.create_new_employee)
            create_employee_button.grid(row=6, column=0, columnspan=2)
            
            reset_customers = tk.Button(self.adminmode, text="Reset Customer Counter", **self.button_style,command=self.reset_customers)
            reset_customers.grid(row=9, column=1, sticky="w")

        if self.isAdmin==2:
            self.current_role_checkbox_var = tk.BooleanVar()
            self.current_role_checkbox = tk.Checkbutton(main, text="Admin", background=WHITE,
                               variable=self.current_role_checkbox_var, command=self.change_password,font=("TkDefaultFont", 15))
            self.current_role_checkbox.grid(row = 2,column = 0,pady = 0)
            self.username_delete_dropdown_var = tk.StringVar()
            self.username_delete_dropdown = ttk.Combobox(self.adminmode, state=READONLY, values = self.usernames, textvariable=self.username_delete_dropdown_var, font=font_style, width=20)
            self.username_delete_dropdown.grid(row=7, column=1, pady=10)
            delete_employee = tk.Button(self.adminmode, text="Delete Employee", **self.button_style,command=self.delete_employee)
            delete_employee.grid(row=8, column=1, sticky="w", pady=(20,0))


        change_password_label = tk.Label(main,text="Change password below", **self.Entry_style)
        change_password_label.grid(row = 1, column = 0, pady=(0,5),sticky=NORTHEASTWEST)

        self.password_entry = tk.Entry(main, show="*",**self.Entry_style)
        self.password_entry.grid(row = 3, column = 0, pady = (0,0),sticky=NORTHEASTWEST)

        self.confirm_password_entry = ttk.Entry(main, show="*", **self.Entry_style )
        self.confirm_password_entry.grid(row = 4, column = 0, pady = (0,10),sticky=NORTHEASTWEST)

        change_password_btn = tk.Button(main, text=f'{"Change role and password" if self.isAdmin == 2 else "Change password"}', **self.button_style, font=font_style, 
                                        command=lambda: self.change_password(self.password_entry.get(), self.confirm_password_entry.get()))
        change_password_btn.grid(row = 5, column = 0, pady = 20,sticky=NORTHEASTWEST)

        exit_btn = tk.Button(main, text="Exit app", **self.button_style, font=font_style, command=self.exit_app)
        exit_btn.grid(row = 6, column = 0, pady = 5)
    def reset_customers(self):
        toggle_topmost(self)
        customers = Customers()
        result = messagebox.askquestion("Confirmation", "Are you sure you want to proceed?")
        if result == "yes":
            customers.reset()
        toggle_topmost(self)

    def set_admin_privileges(self):
        self.newrole = int(self.role_checkbox_var.get())

    def passwords_match(self, password1, password2):
        
        if not any([password1,password2]):
            toggle_topmost(self)
            messagebox.showerror("Not allowed!","Password shouldn't be blank!")
            toggle_topmost(self)
            return False
        if password1 != password2:
            toggle_topmost(self)
            messagebox.showerror("Error", "Passwords do not match!")
            toggle_topmost(self)
            return False
        return True

    def create_new_employee(self):
        if not self.usernameEntry.get() or not self.employee_name.get():
            toggle_topmost(self)
            messagebox.showerror("Cannot be blank", "username/employee name is required!")
            toggle_topmost(self)
            return
        password1 = self.password1.get()
        password2 = self.password2.get()
        username = self.usernameEntry.get()
        if not self.passwords_match(password1, password2):
            return
        query = Login_query()
        toggle_topmost(self)
        if query.add_user(username,password1,self.role_checkbox_var.get()):
            self.usernameEntry.delete(0,END)
            self.password1.delete(0,END)
            self.password2.delete(0,END)

        toggle_topmost(self)

        query = Employees()
        if query.add_employee(self.employee_name.get(),username):
            self.employee_name.delete(0, END)

    def delete_employee(self):
        username = self.username_delete_dropdown_var.get()
        if not username:
            return

        toggle_topmost(self)
        query = Login_query()
        if query.delete_user(username):
            self.username_delete_dropdown["values"] = tuple(
                value for value in self.username_delete_dropdown["values"] if value != username)
            self.username_delete_dropdown_var.set("")
        query = Employees()
        query.delete_employee(username)
        toggle_topmost(self)


    def get_username(self):
        return self.username_var.get()
    def change_password(self, password1, password2):
        if not self.passwords_match(password1, password2):
            return
        username_to_be_changed = self.username 
        if self.isAdmin:
            username_to_be_changed = self.get_username()
        query = Login_query()
        
        role_change = None
        if self.isAdmin==2:
            role_change = self.current_role_checkbox_var.get()

        if username_to_be_changed == self.username:
            role_change = None    
        toggle_topmost(self)
        messagebox.showinfo("Information","You are about to change password. \nIf you are an administrator, please note that you can NOT change your own role. \nThe admin checkbox will not work.")
        if query.change_password(username_to_be_changed,password1,role_change):
            self.password_entry.delete(0, END)
            self.confirm_password_entry.delete(0, END)

        toggle_topmost(self)


    def exit_app(self):
        self.quit()
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
