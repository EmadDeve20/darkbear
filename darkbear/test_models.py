from time import sleep
from paramiko import SSHClient, transport

commands = [
    " apt search tmux\n",
    " ls -lia\n",
]

class Tester:
    """
    A Class With all of the Methods Test about whether the server is a honeypot or not!
    """
    def test(self, cmd: str, output: str):
        """
        test function
        """
        if cmd == commands[0]:
            pass
        if cmd == commands[1]:
            return self.test_is_chrooted(output)

    def test_is_chrooted(self, output: str) -> bool:
        """
        the server chrooted?
        return: true if schrooted
        """

        output = output.split(" ")
        print("output: ", output)
        if output[4] == "1000" and output[5] == "100":
            return True
        return False


class CommandSender:
    def __init__(self, ssh_client: SSHClient) -> None:
        self.ssh_client = ssh_client
        transport = self.ssh_client.get_transport()
        self.channel = transport.open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()
        self.tester = Tester()
        
        print("\nTHE SERVER MESSAGE: ")
        print(self.get_server_msg)
        print("\nSERVER NAME:")
        print(self.get_server_name)

    # TODO: I Tested this function on my ubuntu server and I saw this function can not print all of my server messages!
    @property
    def get_server_msg(self) -> str:
        """
        get the login message from the server
        return: messgae
        """

        server_msg = self.channel.recv(-1).decode()
        sleep(1)
        server_msg += self.channel.recv(-1).decode()
        return self.cut_the_useless_lines(server_msg)

    @property
    def get_server_name(self) -> str:
        """
        get the name of server
        return: server_name
        """

        self.channel.send(" uname -a\n")
        sleep(1)
        return self.cut_the_useless_lines(self.channel.recv(-1).decode())

    def cut_the_useless_lines(self, output: str) -> str:
        """
        cut the first line (your sned command)
        return: everything after first line
        """

        output = output.split("\n")[1:-1]
        return "".join(output)

    def run(self):

        for cmd in commands:

            self.channel.send(cmd)
            sleep(5)
            stdout = self.channel.recv(-1).decode()
            print(f"stdin: {cmd}")
            print(f"stdout: {stdout}")
            print(self.tester.test(cmd, self.cut_the_useless_lines(stdout)))

