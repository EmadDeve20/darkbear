from os import path
from time import sleep
from paramiko import SSHClient, AutoAddPolicy


client = SSHClient()
client.load_system_host_keys()
client.load_host_keys(path.expanduser('~/.ssh/known_hosts'))
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect("127.0.0.1", username='root', password='admin', port=2222)

print("connecting ...")

sleep(1)

client.close()
