import tkinter as tk
from login import Login
from main_page import MainPage
from view_application import ViewApplication
from approve_application import ApproveApplication
from submit_application import SubmitApplication
import tkinter.messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master 
        
        self.master.title("应用程序")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        
        self.master.geometry("600x400")

    def create_widgets(self):
        # 登录界面
        self.login_frame = Login(self)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # 主界面
        self.main_frame = MainPage(self)
        self.main_frame.pack_forget()
        
        self.view_application_frame = ViewApplication(self)
        self.approve_application_frame = ApproveApplication(self) 
        
        self.approve_application_frame.pack_forget()
        self.submit_application_frame = SubmitApplication(self)
        self.submit_application_frame .pack_forget()
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
