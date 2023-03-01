from paramiko import SSHClient, transport

commands = [
    " apt search tmux",
    " ls -lia",
]

class CommandSender:
    def __init__(self, ssh_client: SSHClient) -> None:
        self.ssh_client = ssh_client

    def run(self):



        for cmd in commands:
            transport = self.ssh_client.get_transport()
            channel = transport.open_session()
            channel.get_pty()
            channel.invoke_shell()

            channel.send(cmd)
            stdout = channel.recv(-1)
            print(f"stdin: {cmd}")
            print(f"stdout: {stdout.decode()}")


    