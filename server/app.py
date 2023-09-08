import sqlite3
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import socket
from flask_docs import ApiDoc

app = Flask(__name__)

DATABASE = 'database.db'

#初始化邮件发送数据
smtp_server = ''
smtp_port = 
smtp_username = ''
smtp_password = ''
from_addr = ''
to_addrs = ['', '']
subject = 'title of email'
body = 'this is content of eamil'

#初始化登录用户
user_login = ""

ApiDoc(
    app,
    title="T&V appproval system",
    version="1.0.0",
    description="all API description",
)



# 初始化数据库
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email_address TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS approval (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            applicant TEXT NOT NULL,
            approver TEXT NOT NULL,
            time TEXT NOT NULL,
            appeal_applicant TEXT NOT NULL,
            remark_approver TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'show',
            status_approve TEXT NOT NULL DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

#检测网络
def is_connected():
    # 检测网络连接状态
    try:
        socket.create_connection(('www.baidu.com', 80))
        return True
    except OSError:
        return False
#发送邮件
def send_email(smtp_server, smtp_port, smtp_username, smtp_password, from_addr, to_addrs, subject, body):
    # 检测网络连接状态
    if not is_connected():
        return False, '无网络连接'

    # 设置邮件内容
    msg = MIMEText(body)

    # 设置发送方和接收方
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Subject'] = subject

    # 连接SMTP服务器
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_username, smtp_password)

    try:
        # 发送邮件
        server.sendmail(from_addr, to_addrs, msg.as_string())
        return True, ''
    except Exception as e:
        print('发送邮件失败：', e)
        return False, str(e)
        #失败后再次发送
        send_email(from_addr, to_addrs, msg.as_string())
    finally:
        # 关闭连接
        server.quit()


#根据用户名查找邮箱
def find_email_address(username):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT email_address FROM user WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print("Error connecting to database:", e)
        return str(e)

#根据id查找申请人
def find_applicant(id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM approval WHERE id=?", (id,))
        result = c.fetchone()
        conn.close()
        if result:
            return result
        else:
            return None
    except sqlite3.Error as e:
        print("Error connecting to database:", e)
        return str(e)


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        user_login = username
        if level != "":
            return jsonify({'success': True, 'token': username+"!!!"+"\n待审批数量:"+str(level['pending'])+"\n审批通过率："+str(level['approved_rate'])+'\n你获得称号：'+ title, 'message':'登录成功'})
        else:
            return jsonify({'success': True, 'message': '登录成功！'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

# 注册接口
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email_address = request.json.get('email_address')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO user (username, password, email_address) VALUES (?, ?, ?)", (username, password, email_address))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '注册成功'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': '用户名已存在'})

# 提交申请接口
@app.route('/submit', methods=['POST'])
def submit():
    title = request.json.get('title')
    content = request.json.get('content')
    applicant = request.json.get('applicant')
    approver = request.json.get('approver')
    time = request.json.get('time')
    appeal_applicant = request.json.get('appeal_applicant')
    remark_approver = request.json.get('remark_approver')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=?", (applicant,))
    user = c.fetchone()
    if not user:
        conn.close()
        return jsonify({'success': False, 'message': '申请人不存在'})
    c.execute("SELECT * FROM user WHERE username=?", (approver,))
    user = c.fetchone()
    if not user:
        conn.close()
        return jsonify({'success': False, 'message': '审批人不存在'})
    try:
        c.execute("INSERT INTO approval (title, content, applicant, approver, time, appeal_applicant, remark_approver) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, content, applicant, approver, time, appeal_applicant, remark_approver))
        conn.commit()
        conn.close()
        send_email(smtp_server, smtp_port, smtp_username, smtp_password, from_addr, [find_email_address(approver)],"您收到新申请", "请尽快登录T&V系统处理，\n标题："+title+"\n提交时间"+time)
        return jsonify({'success': True, 'message': '提交成功'})
    except Exception as e:
        conn.close()
        if "SSL: WRONG_VERSION_NUMBER" in str(e):
            send_email(smtp_server, smtp_port, smtp_username, smtp_password, from_addr, [find_email_address(approver)],"您收到新申请", "请尽快登录T&V系统处理，\n标题："+title+"\n提交时间"+time)
            return jsonify({'success': False, 'message': '意外错误，已重新发送'+str(e)})
        else:
            return jsonify({'success': False, 'message': '意外错误'+str(e)})

# 查询申请接口
@app.route('/query_application', methods=['POST'])
def query_application():
    username = request.json.get('username')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM approval WHERE applicant=? AND status='show'", (username,))
    applications = c.fetchall()
    conn.close()
    if applications:
        result = []
        for application in applications:
            result.append({'id': application[0], 'title': application[1], 'content': application[2], 'applicant': application[3], 'approver': application[4], 'time': application[5], 'appeal_applicant':application[6], 'remark_approver':application[7], 'status':application[8], 'status_approve':application[9]})
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'message': '没有申请'})

# 根据ID查询申请接口
@app.route('/query_application_by_id', methods=['POST'])
def query_application_by_id():
    application_id = request.json.get('id')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM approval WHERE id=? AND status='show'", (application_id,))
    application = c.fetchone()
    conn.close()
    if application:
        result = {'id': application[0], 'title': application[1], 'content': application[2], 'applicant': application[3], 'approver': application[4], 'time': application[5], 'appeal_applicant':application[6], 'remark_approver':application[7], 'status':application[8], 'status_approve':application[9]}
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'message': '没有找到该申请'})


# 查询审批接口
@app.route('/query_approval', methods=['POST'])
def query_approval():
    username = request.json.get('username')
    print(f'查询审批参数{username}')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM approval WHERE approver=? AND status='show'", (username,))
    approvals = c.fetchall()
    conn.close()
    if approvals:
        result = []
        for approval in approvals:
            result.append({'id': approval[0], 'title': approval[1], 'content': approval[2], 'applicant': approval[3], 'approver': approval[4], 'time': approval[5], 'appeal_applicant':approval[6], 'remark_approver':approval[7], 'status':approval[8], 'status_approve':approval[9]})
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'message': '没有审批'})

# 删除申请接口
@app.route('/delete_application', methods=['POST'])
def delete_application():
    id = request.json.get('id')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("UPDATE approval SET status='delete' WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '删除成功'})
    except:
        conn.close()
        return jsonify({'success': False, 'message': '意外错误'})

# 申诉申请接口
@app.route('/appeal_application', methods=['POST'])
def appeal_application():
    id = request.json.get('id')
    appeal_content = request.json.get('appeal_content')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("UPDATE approval SET appeal_applicant=?, status_approve='申诉中' WHERE id=?", (appeal_content,id,))
        conn.commit()
        conn.close()
        send_email(smtp_server, smtp_port, smtp_username, smtp_password, from_addr, [find_email_address(find_applicant(id)[3])],"您的申请状态更新", "标题："+find_applicant(id)[1]+"\n状态："+"发起申诉"+"\n提交时间"+find_applicant(id)[5])
        return jsonify({'success': True, 'message': '提交申诉成功'})
    except Exception as e:
        conn.close()
        print(str(e))
        return jsonify({'success': False, 'message': '意外错误'+str(e)})

# 查询用户接口
@app.route('/query_user', methods=['POST'])
def query_user():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT username FROM user")
    users = c.fetchall()
    conn.close()
    if users:
        result = []
        for user in users:
            result.append(user[0])
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'message': '没有用户'})

# 审批申请接口
@app.route('/approve_application', methods=['POST'])
def approve_application():
    id = request.json.get('id')
    status_approve = request.json.get('status_approve')
    remark_approver = request.json.get('remark_approver')
    if remark_approver == "":
        remark_approver == "None"
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("UPDATE approval SET status_approve=?, remark_approver=? WHERE id=?", (status_approve, remark_approver, id))
        conn.commit()
        conn.close()
        approve_details = find_applicant(id)
        send_email(smtp_server, smtp_port, smtp_username, smtp_password, from_addr, [find_email_address(find_applicant(id)[3])],"您的申请状态更新", "标题："+find_applicant(id)[1]+"\n状态："+status_approve+"\n提交时间"+find_applicant(id)[5])
        return jsonify({'success': True, 'message': '审批成功'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': '审批失败'+str(e)})
        
#

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5000)
