import re
import time

import paramiko


class Mikrotik:

    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        if password is None:
            self.password = ""
        else:
            self.password = password
        self.ssh = None  # SSHClient
        self.name = None  # Mikrotik name
        self.connect_ssh()

    def __del__(self):
        if self.ssh:
            self.ssh.close()

    def __str__(self):
        return f"{self.address}({self.name})"

    def connect_ssh(self):
        """Create instance SSHClient for this mikrotik"""
        print(f"Connect to server {self.address}")
        # print(f"user={self.username} | password={self.password}")
        if self.ssh is None:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=self.address, username=self.username, password=self.password, timeout=10, look_for_keys=False)
                transport = ssh.get_transport()
                transport.set_keepalive(30)
                self.ssh = ssh
                print(f"  Successfully connected to server {self.address}")
            except paramiko.AuthenticationException:
                raise Exception(f"ERROR: Authentication failed when connecting to {self.address}")
            except Exception as e:
                raise Exception(f"ERROR: Can't connect to SSH:\n{e}")

    def backup_export(self, backup_name):
        """Create backup with export command.
        Only one copies are stored on the device: the current one."""
        print(f"Create export backup")
        try:
            stdin, stdout, stderr = self.ssh.exec_command(f"/export file={backup_name}\n")
            time.sleep(5)
            print(f"  Export backup created")
        except Exception as e:
            raise Exception(f"ERROR: Can't create export backup:\n{e}")

    def backup_backup(self, backup_name):
        """Create backup with export command.
        Only one copies are stored on the device: the current one."""
        print(f"Create backup backup")
        try:
            stdin, stdout, stderr = self.ssh.exec_command(f"/system backup save name={backup_name}\n")
            time.sleep(5)
            print(f"  Backup backup created")
        except Exception as e:
            raise Exception(f"ERROR: Can't create backup backup:\n{e}")

    def download_file(self, source, destination):
        """Download file from mikrotik"""
        print(f"Download file {source} to {destination}")
        try:
            ftp_client = self.ssh.open_sftp()
            ftp_client.get(source, destination)
            ftp_client.close()
            print(f"  File downloaded")
        except Exception as e:
            raise Exception(f"ERROR: Can't download file:\n{e}")

    def define_name(self):
        """Define name of mikrotik"""
        print(f"Define mikrotik name")
        try:
            stdin, stdout, stderr = self.ssh.exec_command("/system identity print" + "\n")
            output = stdout.read()
            # print(f"output={output.decode('UTF-8')}")
            identity = output.decode('UTF-8').split('name: ')[1].strip()
            self.name = identity[:14]
            print(f"  Name defined")
        except Exception as e:
            raise Exception(f"ERROR: Can't define name:\n{e}")

    def execute_command(self, command):
        """Execute any commands"""
        print(f'Execute command "{command}"')
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command + "\n")
            output = stdout.read()
            output = output.decode('UTF-8')
            print(f"  Command executed:\n-->\n{output}\n-->")
            return output
        except Exception as e:
            raise Exception(f"ERROR: Can't execute command:\n{e}")
