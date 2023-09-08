import requests
import time
import configparser


SERVER_URL = 'http://127.0.0.1:5000'


class ApplicationLogic:

    
    def __init__(self):
        self.applications=[]
    
    #登录逻辑
    def check_login(username,password):
        data={'username':username,'password':password}
        headers={'Content-Type':'application/json'}
        try:
            response=requests.post(f'{SERVER_URL}/login',json=data,headers=headers)
            result=response.json()
            if result['success']:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("网络连接异常:", e)
            return False
    
    #查询申请业务逻辑
    def check_application(username):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{SERVER_URL}/query_application', json={'username':username})
        
        result = response.json()
        return result
    
    #查询审批业务逻辑
    def check_approve_application(username):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{SERVER_URL}/query_approval', json={'username': username}, headers=headers)
        result = response.json()
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return result
            else:
                return False
        else:
            return False
    
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
    def submit_application(title, content, username, approver):
        data = {'title': title, 'content': content, 'applicant': username, 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'approver': approver, 'appeal_applicant':'无', 'remark_approver':'无'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{SERVER_URL}/submit', json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            #print(result)
            if result['success']:
                return True
            else:
                return False
        else:
            return False
	
    # 删除申请
    def delete_application(id):
        headers = {'Content-Type':'application/json'}
        response = requests.post(f'{SERVER_URL}/delete_application', json={'id': id}, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return True
            else:
                return False
        else:
            return False
    
    #申诉申请
    def appeal_application(id, appeal_content):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{SERVER_URL}/appeal_application', json={'id': id, 'appeal_content':appeal_content}, headers=headers)
        result = response.json()
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return True
            else:
                return False
        else:
            return False

	# 审批
    def approve(id, username,status_approve, remark_approver):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{SERVER_URL}/approve_application', json={'id': id, 'approver': username, 'status_approve':status_approve, 'remark_approver':remark_approver}, headers=headers)
        result = response.json()
        #print("运行了"+str(result))
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return True
                #print("成功"+result)
            else:
                return False
                #print(result)
        else:
            return False
            #print(result)
    

    #记住账号和密码
    def save_login_info(username, password):
        # 创建配置文件对象
        config = configparser.ConfigParser()

        # 设置默认值
        config['LOGIN'] = {'username': '', 'password': ''}

        # 读取配置文件
        config.read('login.ini')
        # 更新配置文件
        config.set('LOGIN', 'username', username)
        config.set('LOGIN', 'password', password)
    
        # 保存配置文件
        with open('login.ini', 'w') as f:
            config.write(f)
    
    #记住账号和密码
    def load_login_info():

        # 创建配置文件对象
        config = configparser.ConfigParser()

        # 设置默认值
        config['LOGIN'] = {'username': '', 'password': ''}

        # 读取配置文件
        config.read('login.ini')
        # 从配置文件中读取账号和密码
        username = config.get('LOGIN', 'username')
        password = config.get('LOGIN', 'password')
    
        return username, password    
     
    #加密     
    def encrypt(text, key):
        result = ''
        for char in text:
            result += chr((ord(char) + key) % 256)
        return result

    #解密
    def decrypt(text, key):
        result = ''
        for char in text:
            result += chr((ord(char) - key) % 256)
        return result
    
    
    #计算审批率
    def calculate_approval_rate(username):
        response = requests.post(f'{SERVER_URL}/query_approval', json={'username': username})
    
        if response.json()['success']:
            approvals = response.json()['data']
            approved_count = 0
            total_count = len(approvals)

            if total_count == 0:
                level = '初出茅庐'
                approval_rate = 0
            else:
                for approval in approvals:
                    if approval['status_approve'] == 'approved':
                        approved_count += 1

                approval_rate = approved_count / total_count * 100

                if approval_rate >= 90:
                    level = '正直的'
                elif approval_rate >= 80:
                    level = '公正的'
                elif approval_rate >= 70:
                    level = '中立的'
                elif approval_rate >= 60:
                    level = '稍微有点偏颇的'
                elif approval_rate >= 50:
                    level = '有点偏颇的'
                elif approval_rate >= 40:
                    level = '相当偏颇的'
                elif approval_rate >= 30:
                    level = '非常偏颇的'
                elif approval_rate >= 20:
                    level = '极其偏颇的'
                elif approval_rate >= 10:
                    level = '十恶不赦的'
                else:
                    level = '罪恶滔天的'

            return {'success': True, 'approval_rate': approval_rate, 'level': level}
        else:
            return {'success': True, 'approval_rate': 0, 'level': "初出茅庐"}