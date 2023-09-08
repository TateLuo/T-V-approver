import tkinter as tk
from main_page import MainPage
from view_application import ViewApplication
from approve_application import ApproveApplication
from logic import ApplicationLogic
from submit_application import SubmitApplication
import json

class Login(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        

    def create_widgets(self):
        self.username_label = tk.Label(self, text="用户名:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        self.password_label = tk.Label(self, text="密码:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        # 创建勾选框
        self.remember_me_var = tk.IntVar()
        self.remember_me_checkbutton = tk.Checkbutton(
            self,
            text="记住账号密码",
            variable=self.remember_me_var,
        )
        self.remember_me_checkbutton.pack(fill=tk.BOTH, expand=True)
    
        self.login_button = tk.Button(self, text="登录", command=self.login)
        self.login_button.pack()
        #显示记住的密码
        self.load_login_info()


    def login(self):
        # 用户名密码验证
        #data = json.loads()
        if  ApplicationLogic.check_login(self.username_entry.get(), self.password_entry.get()):
            #记住账号密码
            self.save_login_info()
            
        #if self.username_entry.get() == "admin" and self.password_entry.get() == "admin":
            
            username = self.username_entry.get()
            
            #获取审批率相关信息
            data = ApplicationLogic.calculate_approval_rate(username)
            print(data)
            #设置主页文字信息，用户名、审批率、称号
            self.master.main_frame.update_user_info(username, data['approval_rate'], data['level'])
            
            #向该界面传递参数username
            ViewApplication.get_username(username)
            #根据回传参数判断listbox列表是否已创建，真则刷新，假则新建
            if ViewApplication.is_listbox_created():
                ViewApplication.refresh_data(self.master.view_application_frame)
                
            else:
                ViewApplication.init_treeview_viewApplication(self.master.view_application_frame, username)
            
            #向该界面传递参数username   
            ApproveApplication.get_username(username)
            #根据回传参数判断listbox列表是否已创建，真则刷新，假则新建
            if ApproveApplication.is_listbox_created():
                ApproveApplication.refresh_data(self.master.approve_application_frame)
                
            else:
                ApproveApplication.init_treeview_approveApplication(self.master.approve_application_frame, username)  

            
            SubmitApplication.get_username(username)
            # 登录成功后跳转到主界面
            self.master.main_frame.pack()
            #self.master.view_application_frame.pack()
            self.pack_forget()
        else:
            # 密码错误则提示密码错误
            tk.messagebox.showerror("错误", "用户名或密码错误！")
   
   #点击复选框时事件
    def save_login_info(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.remember_me_var.get():
            if username is not None and password is not None:
                ApplicationLogic.save_login_info(username,password)
            else:
                tk.messagebox.showerror("提示","选择记住用户名密码时，用户名密码不可为空！")
            
        else:
            ApplicationLogic.save_login_info("","")
    
    
    def load_login_info(self):
        # 从配置文件中读取账号和密码
        username = ApplicationLogic.load_login_info()[0]
        password = ApplicationLogic.load_login_info()[1]
    
        if len(username) and len(password):
            # 将账号和密码填入输入框
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
        
            self.remember_me_var.set(1)  # 设置变量的值为1，表示选中状态
            self.remember_me_checkbutton.select()  # 将复选框设置为选中状态
        else:
            self.remember_me_var.set(0)  # 设置变量的值为1，表示选中状态
            self.remember_me_checkbutton.deselect()  # 将复选框设置为选中状态
    
        
            