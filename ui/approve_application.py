import tkinter as tk
from tkinter import ttk
from logic import ApplicationLogic
import tkinter.messagebox
import tkinter.simpledialog as sd
from tkinter import scrolledtext
from PIL import Image, ImageTk

class ApproveApplication(tk.Frame):
    # 定义类变量用户名
    var_username = ""
    # 定义类变量列表是否被创建
    listbox_check = False
    # 定义类变量申请信息
    date_approval = ""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # 显示返回主界面按键
        self.view_application_button = tk.Button(self, text="返回", command=self.backHome)
        self.view_application_button.pack()
        
        # 显示所有待审批申请的列表
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #初始化列表
    
    
    #从登录页面获取用户名
    def get_username(username):
        ApproveApplication.global_var_username = username
        #print (ApproveApplication.global_var_username)
    
    
        #返回listbox列表已创建
    def is_listbox_created():
        return ApproveApplication.listbox_check
        
    
    #初始化列表
    def init_treeview_approveApplication(self, username):
        #定义几个列
        title = ['1','2','3', '4', '5']
        #创建Treeview对象
        self.listbox = ttk.Treeview(self,columns=title, yscrollcommand=self.scrollbar.set, show = 'headings')
        #设置列格式
        self.listbox.column('1',width=60,anchor='center')
        self.listbox.column('2',width=60,anchor='center')
        self.listbox.column('3',width=60,anchor='center')
        self.listbox.column('4',width=60,anchor='center')
        self.listbox.column('5',width=60,anchor='center')
        #设置列标题
        self.listbox.heading("1",text="ID")
        self.listbox.heading("2",text="标题")
        self.listbox.heading("3",text="状态")
        self.listbox.heading("4",text="申请人")
        self.listbox.heading("5",text="时间")
        
        #获取用户的申请信息
        result = ApplicationLogic.check_approve_application(username)
        #print("\n打印审批信息"+str(result))
        if result:
            if result['success']:
                ApproveApplication.date_approval = result['data']
                applications = result['data']
                for application in applications:
                    self.listbox.insert("", "end", values=(application['id'],application['title'], application['status_approve'], application['applicant'],application['time']))
            else:
                self.listbox.insert("", "end", values=("", "","暂无审批"))
        else:
            self.listbox.insert("", "end", values=("", "","暂无审批"))
        #显示列表
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #放进滚动条
        self.scrollbar.config(command=self.listbox.yview)
                 # 创建右键菜单
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="审批", command=self.menu_appovral_application)
        #self.menu.add_command(label="申诉", command=self.menu_appeal_application)
        
        self.listbox.bind('<Button-3>', self.on_right_click)#绑定右键单击事件===========
        self.listbox.bind('<Double-1>', self.on_left_click)#绑定左键双击事件===========
        #用于判断listbox是否创建的
        ApproveApplication.listbox_check = True


        

    #刷新treeview
    def refresh_data(self):
    # 清除 TreeView 中的现有数据
        self.listbox.delete(*self.listbox.get_children())
    
        # 重新加载或更新数据源
        result = ApplicationLogic.check_approve_application(ApproveApplication.global_var_username)  
        # 将新数据添加到 TreeView 中
        if result:
            if result['success']:
                ApproveApplication.date_approval = result['data']
                applications = result['data']
                for application in applications:
                    self.listbox.insert("", "end", values=(application['id'],application['title'], application['status_approve'], application['applicant'],application['time']))
            else:
                self.listbox.insert("", "end", values=("", "","暂无审批"))
        else:
            self.listbox.insert("", "end", values=("", "","暂无审批"))

            
        
    #返回主界面     
    def backHome(self):
        self.master.main_frame.pack()
        self.pack_forget()
    
    #列表右键单击事件
    def on_right_click(self, event):
        # 获取选中的项
        item = self.listbox.identify_row(event.y)
        
        if item:
            # 选择项
            self.listbox.selection_set(item)
            
            # 显示右键菜单
            self.menu.post(event.x_root, event.y_root)
    
    #列表左键双击事件
    def on_left_click(self, event):
        # 获取选中的项
        item = self.listbox.identify_row(event.y)
        
        if item:
            # 选择项
            self.listbox.selection_set(item)
            #获取id号
            for item in self.listbox.selection():
                item_text = self.listbox.item(item,"values")
                #在弹出框展示、
                #print("数据"+str(ViewApplication.date_approval)+"\nid"+item_text[0])
                id = int(item_text[0])
                data = self.find_data_by_id(ApproveApplication.date_approval,id)
                print(data)
                if data['status_approve'] == "pending":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    申请人：{data['applicant']} 
                    状态：{data['status_approve']}
                    时间:{data['time']}
                    '''
                elif data['status_approve'] == "同意":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    申请人：{data['applicant']} 
                    状态：{data['status_approve']}
                    批语：{data['remark_approver']}
                    时间:{data['time']}
                    '''
                elif data['status_approve'] == "不同意":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    申请人：{data['applicant']} 
                    状态：{data['status_approve']}
                    批语：{data['remark_approver']}
                    时间:{data['time']}
                    ''' 
                elif data['status_approve'] == "申诉中":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    审批人：{data['approver']} 
                    状态：{data['status_approve']}
                    批语：{data['remark_approver']}
                    申诉：{data['appeal_applicant']}
                    时间:{data['time']}
                    ''' 
                self.show_long_text_popup("详情", show_text)
            
    #根据ID号找到那一组数据,参数：self、返回的data数据、id号       
    def find_data_by_id(self, data_list, id_num):
        for data in data_list:
            if data['id'] == id_num:
                return data
        return None

    
    #显示长文本弹出窗口
    def show_long_text_popup(self, title, message):
        root = tk.Tk()
        root.withdraw()
        popup = tk.Toplevel(root)
        popup.title(title)
        text = scrolledtext.ScrolledText(popup, width=60, height=20)
        text.insert(tk.END, message)
        # 将文本框中的文本左对齐
        text.tag_configure("left", justify="left")
        text.tag_add("left", "1.0", "end")
        text.pack()
        button = tk.Button(popup, text="关闭", command=popup.destroy)
        button.pack()
        # 获取主窗口的位置和大小
        self.master_x = self.master.winfo_x()
        self.master_y = self.master.winfo_y()
        self.master_width = self.master.winfo_width()
        self.master_height = self.master.winfo_height()

        # 计算弹窗的位置
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        popup_x = self.master_x - popup_width
        popup_y = self.master_y + (self.master_height - popup_height) // 2

        # 设置弹窗的位置
        popup.geometry("+{}+{}".format(popup_x, popup_y))
    
    #菜单键申诉        
    def menu_appovral_application(self):
        for item in self.listbox.selection():
            item_text = self.listbox.item(item,"values")
            #print(item_text)
            self.open_dialog(item_text[0])
    
    #有两个选项的对话框
    def open_dialog(self, id):
        # 创建对话框
        dialog = MyDialog(self, title="批语", prompt="请输入批语内容:")
        # 显示对话框并等待用户操作
        dialog.show()
        if dialog.input_text:
            if dialog.choice == "同意":
                #print(input_text)
                if ApplicationLogic.approve(id, ApproveApplication.global_var_username,"同意", dialog.input_text):
                    tk.messagebox.showinfo("提示","审批成功！")
                else:
                    tk.messagebox.showinfo("提示","审批失败！")
            elif dialog.choice == "不同意":
                #print(input_text)
                if ApplicationLogic.approve(id, ApproveApplication.global_var_username,"不同意", dialog.input_text):
                    tk.messagebox.showinfo("提示","审批成功！")
                else:
                    tk.messagebox.showinfo("提示","审批失败！")
            else:
                tk.messagebox.showinfo("提示","发生错误！")
        else:
            tk.messagebox.showinfo("提示","请输入批语！")
        self.refresh_data()#刷新界面
   


class MyDialog:
    def __init__(self, parent, title=None, prompt=None):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.choice = None
        self.input_text = None

        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(self.title)

        # 创建提示文本和输入框
        tk.Label(self.dialog, text=self.prompt).grid(row=0, column=0, padx=5, pady=5)
        self.entry = tk.Entry(self.dialog)
        self.entry.grid(row=1, column=0, padx=5, pady=5)

        # 创建按钮框架和按钮
        button_frame = tk.Frame(self.dialog)
        button_frame.grid(row=2, column=0, padx=5, pady=5)
        ok_button = tk.Button(button_frame, text="同意", width=10, command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        cancel_button = tk.Button(button_frame, text="不同意", width=10, command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

    def on_ok(self):
        self.choice = "同意"
        self.input_text = self.entry.get()
        self.dialog.destroy()

    def on_cancel(self):
        self.choice = "不同意"
        self.input_text = self.entry.get()
        self.dialog.destroy()

    def show(self):
        # 显示对话框并等待用户操作
        self.parent.wait_window(self.dialog)

#图片弹窗
class PopupWindow:
    def __init__(self, image_path):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.geometry("+300+200")  # 设置弹窗位置
        self.root.bind("<Button-1>", self.close_window)  # 点击任意位置关闭弹窗

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.root, image=photo)
        label.image = photo
        label.pack()

    def close_window(self, event):
        self.root.destroy()