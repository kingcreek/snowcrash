import paramiko
import time

class SSHConnection:
    def __init__(self, username, password):
        self.host = '192.168.0.54'
        self.port = 4242
        self.username = username
        self.password = password
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None

    def connect(self):
        try:
            self.ssh_client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            self.shell = self.ssh_client.invoke_shell()
            time.sleep(1)
            while self.shell.recv_ready():
                self.shell.recv(1024)
        except paramiko.AuthenticationException:
            print("Authentication error. Please check your credentials.")
        except paramiko.SSHException as e:
            print("SSH connection error:", str(e))

    def execute_command(self, command):
        try:
            if self.shell is None:
                print("SSH connection is not established.")
                return None
            
            self.shell.send(command + '\n')
            time.sleep(1)
            output = ""
            while self.shell.recv_ready():
                output += self.shell.recv(1024).decode('utf-8')

            output_lines = output.split('\n')
            output_lines = [line for line in output_lines if not line.startswith(command)]
            output_lines = [line for line in output_lines if not line.endswith('$ ')]

            return output_lines
        except paramiko.SSHException as e:
            print("Error executing command:", str(e))

    def close(self):
        self.ssh_client.close()
