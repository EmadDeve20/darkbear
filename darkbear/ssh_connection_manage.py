from os import path
from paramiko import SSHClient, AutoAddPolicy

def ssh_connect(host: str, port: int, username: str, password: str, known_host_file: str) -> SSHClient:
    
    client = SSHClient()
    client.load_system_host_keys()

    known_host_file = path.expanduser(known_host_file)
    client.load_host_keys(path.expanduser(known_host_file))
    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(hostname=host, port=port, username=username, password=password)
    return client