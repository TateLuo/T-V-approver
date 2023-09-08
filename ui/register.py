import requests

# 服务端地址
SERVER_URL = 'http://127.0.0.1:5000'

# 注册函数
def register():
    username = input('Please enter your username: ')
    password = input('Please enter your password: ')
    response = requests.post(f'{SERVER_URL}/register', data={'username': username, 'password': password})
    result = response.json()
    if result['success']:
        print('Registration successful')
    else:
        print(f'Registration failed: {result["message"]}')

# 主函数
if __name__ == '__main__':
    register()
