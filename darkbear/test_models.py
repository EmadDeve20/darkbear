from time import sleep
from paramiko import SSHClient, transport

commands = [
    " apt search tmux\n",
    " ls -lia\n",
]

class CommandSender:
    def __init__(self, ssh_client: SSHClient) -> None:
        self.ssh_client = ssh_client
        transport = self.ssh_client.get_transport()
        self.channel = transport.open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()
        
        print("\nTHE SERVER MESSAGE: ")
        print(self.get_server_msg)
        print("\nSERVER NAME:")
        print(self.get_server_name)

    @property
    def get_server_msg(self) -> str:
        """
        get the login message from the server
        return: messgae
        """

        return self.channel.recv(-1).decode()


    @property
    def get_server_name(self) -> str:
        """
        get the name of server
        return: server_name
        """

        self.channel.send(" uname -a\n")
        sleep(1)
        return self.channel.recv(-1).decode()

    def run(self):

        for cmd in commands:

            self.channel.send(cmd)
            sleep(5)
            stdout = self.channel.recv(-1)
            print(f"stdin: {cmd}")
            print(f"stdout: {stdout.decode()}")

