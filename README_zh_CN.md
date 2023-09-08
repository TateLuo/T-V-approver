# T&V 审批系统
 一个纯Python的Windows桌面程序，用于提交审批和审批，有服务器和图形界面客户端

- en [English](README.md)
- zh_CN [简体中文](README.zh_CN.md)


＃＃＃ 用法
1.下载源码、ui和服务器
2. 依次安装所需Python模块
3. 在你的云服务器上部署app.py，并在app.py中设置邮件host信息和服务器host信息
4. 在logic.py中设置host信息并通过Pyinstaller将main.py打包为GUI程序
[下载 GUI的Pyinstaller](https://pypi.org/project/auto-py-to-exe/#files)

PS：由于是个人使用，所以我没有再GUI中设计登录的功能，但是单独写了个register.py可以用来注册
