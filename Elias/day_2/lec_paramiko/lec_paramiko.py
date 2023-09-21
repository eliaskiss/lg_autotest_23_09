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

    ################################################################
    # Put File to Host (SFTP)
    # scrFilePath: Local(PC, Client), dstFilePath: Server(host)
    ################################################################
    def putToHost(self, srcFilePath, dstFilePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.put(srcFilePath, dstFilePath)

    ###############################################################
    # Rename file on Host (SFTP)
    # srcFilePath: Old Name, dstFilePath: New Name
    ###############################################################
    def renameHostFile(self, srcFilePath, dstFilePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.rename(srcFilePath, dstFilePath)

    ###############################################################
    # Delete file on Host (SFTP)
    # filePath: Server(host)
    ###############################################################
    def deleteHostFile(self, filePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.remove(filePath)

    ###############################################################
    # Get file list on Host (SFTP)
    # filePath: Server(host)
    ###############################################################
    def getFileListFromHost(self, filePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        return self.ftp_client.listdir(filePath)

    ######################################################################
    # Get file list of host
    # srcFilePath: Server(host)
    ###############################################################
    def getFileAttrListFromHost(self, srcFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        return self.ftp_client.listdir_attr(srcFilePath)

    ###############################################################
    # Delete folder of host
    # srcFilePath: Server(host)
    ###############################################################
    def deleteHostFolder(self, srcFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()

        # # Only current folder only
        # file_list = self.getFileListFromHost(srcFilePath)
        # for file in file_list:
        #     file_path = os.path.join(srcFilePath, file)  # srcFilePath /var/www  filename: log.txt -> /var/www/log.txt
        #     file_path = file_path.replace('\\', '/')
        #     self.deleteHostFile(file_path)

        # Delete all subfolder recursive
        file_attr_list = self.ftp_client.listdir_attr(srcFilePath)
        for file_attr in file_attr_list:
            path = os.path.join(srcFilePath, file_attr.filename)
            path = path.replace('\\', '/')
            # Path is Folder type
            if stat.S_ISDIR(file_attr.st_mode):
                self.deleteHostFolder(path)
            # Path is File type
            else:
                self.deleteHostFile(path)

        self.ftp_client.rmdir(srcFilePath)  # rm -rf target_folder

    ###############################################################
    # Get file from host with SCP
    # scrFilePath: Server(host), dstFilePath: Local(PC, Client)
    ###############################################################
    def getFromHostWithSCP(self, srcFilePath, dstFilePath):
        if self.scp_client is None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.get(srcFilePath, dstFilePath)

    ###############################################################
    # Put file to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    ###############################################################
    def putToHostWithSCP(self, srcFilePath, dstFilePath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.put(srcFilePath, dstFilePath)

    ###############################################################
    # Get folder to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    ###############################################################
    def getFolderToHostSCP(self, srcDirPath, dstDirPath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.get(srcDirPath, dstDirPath, recursive=True)

    ###############################################################
    # Put folder to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    ###############################################################
    def putFolderToHostSCP(self, srcDirPath, dstDirPath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.put(srcDirPath, dstDirPath, recursive=True)

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

            # ############################################################
            # # > cd temp
            # # > ls -al
            # ############################################################
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
            # ssh.sudoCommand('mkdir /elias')

            # ############################################################
            # # 서버로 부터 파일 가져오기
            # ############################################################
            # ssh.getFromHost('./process_list.txt', 'process_list.txt')

            # ############################################################
            # # 서버로 파일 업로드 하기
            # ############################################################
            # ssh.putToHost('./process_list_2.txt', 'process_list_2.txt')

            # ############################################################
            # # 서버에 있는 파일명 변경
            # ############################################################
            # ssh.renameHostFile('./process_list.txt', './process.txt')
            # ssh.renameHostFile('./temp', './temp2')

            # ############################################################
            # # 서버에 있는 파일 삭제
            # ############################################################
            # ssh.deleteHostFile('./process.txt')

            # ############################################################
            # # 서버에 있는 폴더내 파일목록 가져오기
            # ############################################################
            # file_list = ssh.getFileListFromHost('./temp2')
            # for file in file_list:
            #     print(file)

            # ############################################################
            # # 서버에 있는 폴더내 파일목록 및 속성 가져오기
            # ############################################################
            # file_list = ssh.getFileAttrListFromHost('./temp2')
            # for file in file_list:
            #     print(file)

            # ############################################################
            # # 서버에 있는 폴더내 삭제
            # ############################################################
            # ssh.deleteHostFolder('./temp2')


            ############################################################
            # Disconnect From Server
            ############################################################
            ssh.disconnect()

        else:
            ic('Connection is failed')
    except Exception as e:
        message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
        ic(message)




























