import tkinter as tk
from view_application import ViewApplication
from approve_application import ApproveApplication
from submit_application import SubmitApplication

class MainPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        #三个主要功能界面
        

    def create_widgets(self):
        # 显示用户信息
        self.user_info_label = tk.Label(self, text="")
        self.user_info_label.pack()
  
        # 显示三个按键
        self.view_application_button = tk.Button(self, text="查看申请", command=self.view_application)
        self.view_application_button.pack()
        self.approve_application_button = tk.Button(self, text="审批申请", command=self.approve_application)
        self.approve_application_button.pack()
        self.submit_application_button = tk.Button(self, text="提交新申请", command=self.submit_application)
        self.submit_application_button.pack()
        self.submit_application_button = tk.Button(self, text="退出登录", command=self.bacl_login)
        self.submit_application_button.pack()

        # 子界面框架
        self.sub_frame = tk.Frame(self)
        
    def view_application(self):
        #self.master.show_view_application
        # 点击查看申请按钮显示查看申请界面
        self.master.view_application_frame.pack()
        self.pack_forget()
        self.master.approve_application_frame.pack_forget()
        self.master.submit_application_frame.pack_forget()
        ViewApplication.refresh_data(self.master.view_application_frame)
        
        
    def approve_application(self):
        # 点击审批申请按钮显示审批申请界面
        self.master.approve_application_frame.pack()
        self.pack_forget()
        self.master.view_application_frame.pack_forget()
        self.master.submit_application_frame.pack_forget()
        ApproveApplication.refresh_data(self.master.approve_application_frame)

    def submit_application(self):
        # 点击提交新申请按钮显示提交新申请界面
        self.master.submit_application_frame.pack()
        self.master.view_application_frame.pack_forget()
        self.master.approve_application_frame.pack_forget()
        self.pack_forget()

    def update_user_info(self, username, approval_rate, title):
        # 更新用户信息显示
        user_info_text = "当前用户：{}\n审批通过率：{}\n称号：{}".format(username, approval_rate, title)
        self.user_info_label.config(text=user_info_text)
        
    def bacl_login(self):
        self.master.login_frame.pack()
        self.pack_forget()
        self.master.approve_application_frame.pack_forget()
        self.master.submit_application_frame.pack_forget()
        self.master.view_application_frame.pack_forget()
