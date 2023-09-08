import tkinter as tk
from tkinter import ttk
from logic import ApplicationLogic
import tkinter.messagebox
import tkinter.simpledialog as sd
from tkinter import scrolledtext
import json

class ViewApplication(tk.Frame):
    # 定义类变量用户名
    var_username = ""
    # 定义类变量列表是否被创建
    listbox_check = False
    # 定义类变量申请信息
    date_approval = ""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.listbox = None  # 初始化实例变量
        self.create_widgets()
        
    def show_selected_item(event):
        selected_item = self.listbox.get(self.listbox.curselection())
        messagebox.showinfo("Selected Item", selected_item)        

    def create_widgets(self):
        # 显示返回主界面按键
        self.view_application_button = tk.Button(self, text="返回", command=self.backHome)
        self.view_application_button.pack(side='top')
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        
    #从登录页面获取用户名
    def get_username(username):
        ViewApplication.var_username = username 
        #print (ViewApplication.var_username + username)
    
    #返回listbox列表已创建
    def is_listbox_created():
        return ViewApplication.listbox_check
    
    #初始化列表
    def init_treeview_viewApplication(self, username):
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
        self.listbox.heading("4",text="审批人")
        self.listbox.heading("5",text="时间")
        
        #获取用户的申请信息
        result = ApplicationLogic.check_application(username)
     
        if result:
            #print("查看申请获取的结果"+ str(result))
           
            if result['success']:
                ViewApplication.date_approval = result['data']
                applications = result['data']
                for application in applications:
                    self.listbox.insert("", "end", values=(application['id'],application['title'], application['status_approve'], application['approver'],application['time']))
            else:
                self.listbox.insert("", "end", values=("", "","暂无申请"))
        else:
            messagebox.showinfo("提示", "出现错误返回首页")
        #显示列表
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #放进滚动条
        self.scrollbar.config(command=self.listbox.yview)
        print('查看申请界面运行了')
        
         # 创建右键菜单
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="删除", command=self.menu_delete_application)
        self.menu.add_command(label="申诉", command=self.menu_appeal_application)
        
        self.listbox.bind('<Button-3>', self.on_right_click)#绑定右键单击事件===========
        self.listbox.bind('<Double-1>', self.on_left_click)#绑定左键双击事件===========
        #改变列表是否创建检查变量状态
        ViewApplication.listbox_check = True
        
        
    #刷新treeview
    def refresh_data(self):
        #print("当前用户名"+ViewApplication.global_var_username)
        # 清除 TreeView 中的现有数据
        self.listbox.delete(*self.listbox.get_children())
    
        # 重新加载或更新数据源
        result = ApplicationLogic.check_application(ViewApplication.var_username)
        
        if result:
            if result['success']:
                ViewApplication.date_approval = result['data']
                applications = result['data']
                for application in applications:
                    self.listbox.insert("", "end", values=(application['id'],application['title'], application['status_approve'], application['approver'],application['time']))
            else:
                self.listbox.insert("", "end", values=("", "","暂无申请"))
        else:
            self.listbox.insert("", "end", values=("", "","暂无申请"))

        
        
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
                data = self.find_data_by_id(ViewApplication.date_approval,id)
                if data['status_approve'] == "pending":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    审批人：{data['approver']} 
                    状态：{data['status_approve']}
                    时间:{data['time']}
                    '''
                elif data['status_approve'] == "同意":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    审批人：{data['approver']} 
                    状态：{data['status_approve']}
                    批语：{data['remark_approver']}
                    时间:{data['time']}
                    '''
                elif data['status_approve'] == "不同意":
                    show_text = f'''
                    标题：{data['title']}
                    内容：{data['content']}
                    审批人：{data['approver']} 
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

    
    #菜单键删除        
    def menu_delete_application(self):
        for item in self.listbox.selection():
            item_text = self.listbox.item(item,"values")
            reslut = ApplicationLogic.delete_application(item_text[0])
            if reslut:
                tk.messagebox.showinfo("提示","申诉删除成功！")
            else:
                tk.messagebox.showinfo("提示","申诉删除失败！")
            print("审批"+item_text[0])
        self.refresh_data()#刷新界面
    
    #菜单键申诉    
    def menu_appeal_application(self):
        for item in self.listbox.selection():
            item_text = self.listbox.item(item,"values")
            print("申诉"+item_text[0])            
            self.open_dialog(item_text[0])
            
        

    #带输入框的弹出对话框
    def open_dialog(self, id):
        # 创建对话框
        value = sd.askstring("输入", "请输入申诉理由")
        
        if value is not None:
            # 用户输入了文本
            print(f"用户输入了：{value}")
            reslut = ApplicationLogic.appeal_application(id, value)
            if reslut:
                tk.messagebox.showinfo("提示","申诉提交成功！")
            else:
                tk.messagebox.showinfo("提示","申诉提交失败！")
        else:
            # 用户取消了对话框
            print("用户取消了对话框")
        self.refresh_data()#刷新界面
    
    
    
    


#自定义对话框
class MyDialog(sd.Dialog):
    def __init__(self, parent):
        self.result = None
        
        super().__init__(parent, title="确认")
        
    def body(self, master):
        # 创建标签和输入框
        tk.Label(master, text="请输入一些文本：").grid(row=0, column=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1)
        
        # 创建两个按钮
        self.yes_button = tk.Button(master, text="同意", command=self.on_yes)
        self.yes_button.grid(row=1, column=0)
        
        self.no_button = tk.Button(master, text="不同意", command=self.on_no)
        self.no_button.grid(row=1, column=1)

    def on_yes(self):
        # 用户点击了“同意”
        self.result = "同意"
        self.destroy()

    def on_no(self):
        # 用户点击了“不同意”
        self.result = "不同意"
        self.destroy()            