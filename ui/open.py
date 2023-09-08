import requests
import json
import time
from turtle import *
from random import *
from math import *
	
	

	
	
class ApplicationLogic:
    def __init__(self):
    #SERVER_URL = 'http://104.243.17.240:5000'
    SERVER_URL = 'http://127.0.0.1:5000'
    TOKEN = "" 
	# 登录
	def login(self, username, password):
	    data = {'username': username, 'password': password}
	    headers = {'Content-Type': 'application/json'}
	    
	    try:
	        response = requests.post(f'{SERVER_URL}/login', json=data, headers=headers)
	        result = response.json()
	        
	        if result['success']:
	            TOKEN = result['token']
	            print(f'登录成功 欢迎你{TOKEN}！！！\n')
	            return username
	        else:           
	            print('登录失败：', result['message'])
	
	            return None
	    except requests.exceptions.RequestException as e:
	        print('网络错误：', e)
	        return None
	    except ValueError as e:
	        print('解析响应数据错误：', e)
	        return None
            
	# 查询申请
	def query_applications(username):
	    headers = {'Content-Type': 'application/json'}
	    response = requests.post(f'{SERVER_URL}/query_application', json={'username': username})
	    result = response.json()
	    
	    if result['success']:
	        applications = result['data']
	        print('申请列表：\n')
	        
	        print('| ID | 标题 | 状态 | 时间                |')
	        print('|----|-----|------|---------------------|')
	        
	        for application in applications:
	            print(f'| {application["id"]}  | {application["title"]} | {application["status_approve"]} | {application["time"]} |')
	        
	        if len(applications) == 0:
	            print('\n没有申请')
	        else:
	            id = input('\n请输入要查看或删除的申请 ID（按回车键取消）：')
	            
	            if id:
	                details_data = query_application_by_id(id)
	                print(f"\n### 申请详情\n")
	                print(f"**标题：** {details_data['title']}  ")
	                print(f"**内容：** {details_data['content']}  ")
	                print(f"**审批人：** {details_data['approver']}  ")
	                print(f"**申请人：** {details_data['applicant']}  ")
	                if details_data['remark_approver'] != "无":
	                    print(f"**批语：** {details_data['remark_approver']}  ")
	                if details_data['appeal_applicant'] !="无" and details_data['status_approve'] == "申诉中":
	                    print(f"**批语：** {details_data['appeal_applicant']}  ")
	                print(f"**时间：** {details_data['time']}  ")
	                
	                choice = input('\n请选择操作（输入数字）：\n1. 删除\n2. 申诉\n\n3. 返回\n')
	                
	                if choice == '1':
	                    delete_application(id)
	                elif choice == '2':
	                    appeal_content = input('\n请输入你的申诉理由（按回车键取消）：')
	                    if appeal_content:
	                        appeal_application(id,appeal_content)
	                    else:
	                        appeal_application(id,"无")
	    else:
	        print('查询失败：', result['message'])
	# 查询申请详情
	def query_application_by_id(application_id):
	    url = SERVER_URL+'/query_application_by_id'
	    data = {'id': application_id}
	    response = requests.post(url, json=data)
	    
	    if response.status_code == 200:
	        result = response.json()
	        
	        if result['success']:
	            return result['data']
	        else:
	            print(result['message'])
	    else:
	        print('请求失败')
	
	# 删除申请
	def delete_application(id):
	    headers = {'Content-Type': 'application/json'}
	    response = requests.post(f'{SERVER_URL}/delete_application', json={'id': id}, headers=headers)
	    result = response.json()
	    
	    if result['success']:
	        print('删除成功')
	    else:
	        print('删除失败：', result['message'])
	        # 申诉申请
	def appeal_application(id, appeal_content):
	    headers = {'Content-Type': 'application/json'}
	    response = requests.post(f'{SERVER_URL}/appeal_application', json={'id': id, 'appeal_content':appeal_content}, headers=headers)
	    result = response.json()
	    
	    if result['success']:
	        print('提交申诉成功')
	    else:
	        print('提交申诉失败：', result['message'])
	#查看审批
	def approve_application(username):
	    headers = {'Content-Type': 'application/json'}
	    response = requests.post(f'{SERVER_URL}/query_approval', json={'username': username}, headers=headers)
	    result = response.json()
	    print(username)
	
	    if result['success']:
	        applications = result['data']
	        print('待审批列表：')
	        print('-------------------------')
	
	        for application in applications:
	            print(f'ID：{application["id"]}')
	            print(f'标题：{application["title"]}')
	            print(f'内容：{application["content"]}')
	            print(f'申请人：{application["applicant"]}')
	            print(f'申请时间：{application["time"]}')
	            print(f'申请状态：{application["status_approve"]}')
	            if "申诉" in application['status_approve']:
	                print(f'申诉内容：{application["appeal_applicant"]}')
	            print('-------------------------')
	
	        if len(applications) == 0:
	            print('没有待审批的申请')
	        else:
	            id = input('请输入要审批的申请 ID（按回车键取消）：')
	
	            if id:
	                choice = input('输入1同意，输入2不同意（按回车键取消）：')
	
	                if choice == '1':
	                    remarks = input('请输入批语（按回车键取消）')
	                    if remarks:
	                        approve(id, username, "同意", remarks)
	                    elif remarks == "":
	                        approve(id, username, "同意", "无")
	                    #打印一个名字组成的心
	                    print('\n'.join([''.join([(username[(x-y) % len(username)]if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ')for x in range(-30, 30)])for y in range(30, -30, -1)]))
	                    print('非常感谢！')
	                elif choice == '2':
	                    remarks = input('请输入批语（按回车键取消）')
	                    if remarks:
	                        approve(id, username, "不同意", remarks)
	                    elif remarks == "":
	                        approve(id, username, "不同意", "无")
	                    print('已拒绝该申请')
	
	# 审批
	def approve(id, username,status_approve, remark_approver):
	    headers = {'Content-Type': 'application/json'}
	    response = requests.post(f'{SERVER_URL}/approve_application', json={'id': id, 'approver': username, 'status_approve':status_approve, 'remark_approver':remark_approver}, headers=headers)
	    result = response.json()
	    
	    if result['success']:
	        print('审批成功')
	    else:
	        print('审批失败：', result['message'])
	        #查询所有用户
	def query_user():
	    url = SERVER_URL+"/query_user"
	    response = requests.post(url)
	    
	    if response.status_code == 200:
	        result = response.json()
	        
	        if result['success']:
	            return result['data']
	        else:
	            print(result['message'])
	    else:
	        print('请求失败')
	# 提交申请
	def submit_application(username):
	    title = input('请输入申请标题：')
	    content = input('请输入申请内容：')
	    users = query_user()
	    
	    print('请选择审批人：')
	    
	    for i, user in enumerate(users):
	        print(f'{i+1}. {user}')
	    
	    choice = input('请输入数字选择：')
	    if isinstance(choice,int) & 0 < int(choice) <= int(len(users)):
	        approver = users[int(choice)-1]
	        print(f'你选择的审批人为：{approver}')
	    
	        data = {'title': title, 'content': content, 'applicant': username, 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'approver': approver, 'appeal_applicant':'无', 'remark_approver':'无'}
	    
	        headers = {'Content-Type': 'application/json'}
	        response = requests.post(f'{SERVER_URL}/submit', json=data, headers=headers)
	        result = response.json()
	    
	        if result['success']:
	            print('提交成功')
	        else:
	            print('提交失败：', result['message'])
	    else:
	        print('输入有误哦，重新输入吧！')
	        submit_application(username)
	