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
        pass









if __name__ == '__main__':
    ssh = MySSH()

    try:
        if ssh.connect('45.115.155.124', 'elias', 'lguser', timeout=5, port=22):
            ic('SSH is connected')
        else:
            ic('Connection is failed')
    except Exception as e:
        message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
        ic(message)




























