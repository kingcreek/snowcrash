import sys
sys.path.append('../')
import codecs
from sshconnector import SSHConnection

# Tool used to detect encryption https://www.cachesleuth.com/multidecoder/ (select focus mode)

def rot_11_decode(text):
    decoded_text = ""
    for char in text:
        if 'a' <= char <= 'z':
            decoded_text += chr((ord(char) - ord('a') + 11) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            decoded_text += chr((ord(char) - ord('A') + 11) % 26 + ord('A'))
        else:
            decoded_text += char
    return decoded_text

username = 'level00'
password = 'level00'

sshconn = SSHConnection(username, password)

print("Conencting ssh...")
sshconn.connect()

print("Find in '/' path all files from user flag00")
stdout = sshconn.execute_command('find / -user flag00 2>/dev/null')

password = None

# print(f"file {stdout}")

for line in stdout:
    print(f"file {line.strip()}")
    fileContent = sshconn.execute_command('cat ' + line.strip())[0]
    print(f"content {fileContent}")
    password = rot_11_decode(fileContent)
    print(f"Decoded ROT11: {password}")

print("Try connect with su flagg00")
stdout = sshconn.execute_command('su flag00')[0]
if stdout == 'Password: ':
    passresult = sshconn.execute_command(password)
    nextflag = sshconn.execute_command("getflag")
    print(f"{nextflag[0]}")

sshconn.close()

