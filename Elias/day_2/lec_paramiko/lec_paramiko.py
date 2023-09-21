import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os
import stat
import time
from icecream import ic
import sys

ic.configureOutput(includeContext=True)

class MySSH:
    def __init__(self):
        self.ftp_client = None  # For SFTP
        self.client = None      # For SSH
        self.scp_client = None  # For SCP
        self.password = None

    ########################################################
    # Check Connection
    ########################################################
    def isAlive(self):
        if self.client is None:
            return False
        else:
            return self.client.get_transport().is_active()

    ########################################################
    # Connect Host
    ########################################################
    def connect(self, host, user_id, user_password, port=22, timeout=None):
        if self.client is None:
            self.client = SSHClient()
            
            # 이코드가 없으면 'Server ... not found in known_hosts' 예외발생
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=host, port=port, username=user_id, password=user_password,
                                timeout=timeout)

            if self.isAlive():
                self.password = user_password
                return True
            else:
                return False

    ########################################################
    # Execute Shell Command
    ########################################################
    def exeCommand(self, command, isReturn = False):
        if self.isAlive():
            # _, stdout, _ = self.client.exec_command(command)
            stdin, stdout, stderr = self.client.exec_command(command)

            error_list = stderr.readlines()
            if len(error_list) != 0:
                print('Errors occurs')
                print(error_list)

            if isReturn is True:
                return stdout.readlines()
        else:
            ic('Client is not connected!!!')

    ########################################################
    # Execute sudo Shell Command
    ########################################################
    def sudoCommand(self, command, isReturn = False):
        if self.isAlive():
            stdin, stdout, stderr = self.client.exec_command('sudo ' + command, get_pty=True)

            stdin.write(self.password + '\n')
            time.sleep(0.1)

            error_list = stderr.readlines()
            if len(error_list) != 0:
                print('Errors occurs')
                print(error_list)

            if isReturn is True:
                return stdout.readlines
        else:
            ic('Client is not connected!!!')

    ########################################################
    # Disconnect
    ########################################################
    def disconnect(self):
        if self.client is not None:
            self.client.close()

    ########################################################
    # Get File from Host (SFTP)
    # srcFilePath: Server(host), dstFilePath: Local(PC, Client)
    ########################################################
    def getFromHost(self, srcFilePath, dstFilePath):
        if self.ftp_client is None:
            if self.client is not None:
                self.ftp_client = self.client.open_sftp()
            else:
                ic('SSH is not connected!!!')
        self.ftp_client.get(srcFilePath, dstFilePath)








if __name__ == '__main__':
    ssh = MySSH()

    try:
        if ssh.connect('45.115.155.124', 'elias', 'lguser', timeout=5, port=22):
            ic('SSH is connected')
            
            # ############################################################
            # # Process List 파일생성 (ps -ef > process_list.txt)
            # ############################################################
            # ssh.exeCommand('ps -ef > process_list.txt', False)

            # ############################################################
            # # 파일목록 가져오기 (ls -al)
            # ############################################################
            # file_list = ssh.exeCommand('ls -al', True)
            # for file in file_list:
            #     print(file, end='')

            ############################################################
            # > cd temp
            # > ls -al
            ############################################################
            # ssh.exeCommand('cd temp')
            # file_list = ssh.exeCommand('ls -al', True)
            # for file in file_list:
            #     print(file, end='')

            '''
            ; - 앞의 명령어가 실패해도 다음 명령어가 실행
            && - 앞의 명령어가 성공했을 때 다음 명령어가 실행
            & - 앞의 명령어를 백그라운드로 돌리고 동시에 뒤의 명령어를 실행
            https://opentutorials.org/module/2538/15818
            '''
            # output_list = ssh.exeCommand('cd temp && ls -al && pwd', True)
            # # Error 발생시
            # # output_list = ssh.exeCommand('cd temp2 && ls -al && pwd', True)
            # for output in output_list:
            #     print(output, end='')

            # ############################################################
            # # Shell Script 파일생성 및 실행
            # ############################################################
            # ssh.exeCommand('echo "ps -ef > process_list.txt" > make_process_list.sh')
            # ssh.exeCommand('chmod +x ./make_process_list.sh')
            # ssh.exeCommand('./make_process_list.sh')

            ############################################################
            # sudo command 실행
            ############################################################
            # ssh.exeCommand('sudo mkdir /myfolder')
            ssh.sudoCommand('mkdir /elias')

            ############################################################
            # Disconnect From Server
            ############################################################
            ssh.disconnect()















        else:
            ic('Connection is failed')
    except Exception as e:
        message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
        ic(message)




























