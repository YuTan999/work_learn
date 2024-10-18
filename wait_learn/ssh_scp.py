#!/usr/bin/env python
# coding=UTF-8
'''
Created on 2021-08-17
@author: yingjiel
'''
import paramiko
from scp import SCPClient
import argparse
import os
import socket
from contextlib import closing


class ssh_and_scp(object):
   def __init__(self, host, port, username, password):
      # 服务端相关配置
      self.host = host
      self.port = port
      self.username = username
      self.password = password
      self.sshClien = None

   def connect(self):
      self.sshClien = paramiko.SSHClient()
      self.sshClien.load_system_host_keys()
      self.sshClien.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.sshClien.connect(self.host, self.port, self.username, self.password)
   def disconnect(self):
      if(self.sshClien == None):
         print("without ssh is connect")
         return -1
      self.sshClien.close()
      self.sshClien = None
   # 发送本地文件到远端
   def sendFile2Remote(self, local_file, remote_file):
      if(self.sshClien == None):
         print("please connet ssh first")
         return -1
      # 创建scp
      with SCPClient(self.sshClien.get_transport()) as scp:
         scp.put(local_file, remote_file)
   # 从远端拉文件
   def getFileFromRemote(self, local_file, remote_file):
      if(self.sshClien == None):
         print("please connet ssh first")
         return -1
      # 创建ssh访问
      # 创建scp
      with SCPClient(self.sshClien.get_transport()) as scp:
         scp.get( remote_file, local_file)
   # 发送命令
   def sendCommand(self, command):
      if(self.sshClien == None):
         print("please connet ssh first")
         return -1
      self.sshClien.exec_command(command)


# 下面是例子
def example():
   ssh_scp = ssh_and_scp('192.168.168.14', 22, 'root', '123456')
   ssh_scp.connect()
   # scp.sendFile2Remote(r'C:\Users\yingjie.lin\Desktop\AutoUpdate\AutoUpdate2.py', '/tmp/testFile')
   ssh_scp.getFileFromRemote(r'C:\Users\yingjie.lin\Desktop\AutoUpdate\AutoUpdate3.py', '/tmp/testFile')
   ssh_scp.sendCommand(r"date > /tmp/testTime")
   ssh_scp.disconnect()

if __name__ == '__main__':
   example()
