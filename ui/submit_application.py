import tkinter as tk
from tkinter import ttk
from logic import ApplicationLogic
import tkinter.messagebox

class SubmitApplication(tk.Frame):
    #定义一个类变量
    username = ""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # 显示返回主界面按键
        self.view_application_button = tk.Button(self, text="返回", command=self.back_home)
        self.view_application_button.pack()
        
        # 输入申请标题、申请内容、选择审批人等信息
        self.title_label = tk.Label(self, text="申请标题:")
        self.title_label.pack()
        
        self.title_entry = tk.Entry(self)
        self.title_entry.pack()
        
        self.content_label = tk.Label(self, text="申请内容:")
        self.content_label.pack()
        
        self.content_textbox = tk.Text(self, height=10)
        self.content_textbox.pack()
        
        self.approver_label = tk.Label(self, text="选择审批人:")
        self.approver_label.pack()
        
        #下拉框
        self.approver_combobox = ttk.Combobox(self, values=ApplicationLogic.query_user())
        self.approver_combobox.pack()
        
        # 显示返回主界面按键
        self.submit_button = tk.Button(self, text="提交申请", command=self.submit)
        self.submit_button.pack()
        
        
    def back_home(self):
        """
        返回主界面
        """
        self.master.main_frame.pack()
        self.pack_forget()
    
    def submit(self):
        """
        提交申请
        """
        title = self.title_entry.get()
        content = self.content_textbox.get("1.0", "end-1c")
        approver = self.approver_combobox.get()
        
        if not title:
            tk.messagebox.showerror("错误", "申请标题不能为空！")
            return
        
        if not content:
            tk.messagebox.showerror("错误", "申请内容不能为空！")
            return
        
        if not approver:
            tk.messagebox.showerror("错误", "请选择审批人！")
            return
        
        if ApplicationLogic.submit_application(title, content, SubmitApplication.username, approver):
            tk.messagebox.showinfo("提示", "提交成功！")
            self.back_home()
        else:
            tk.messagebox.showerror("提示", "提交失败！")
    
    #从登录页面获取用户名
    def get_username(username):
        SubmitApplication.username = username