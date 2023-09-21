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

            self.client.connect(hostname=host, port=port, username=user_id, password=user_password,
                                timeout=timeout)

            if self.isAlive():
                self.password = user_password
                return True
            else:
                return False































