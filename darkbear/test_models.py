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
    report_lists = []
    def test(self, cmd: str, output: str):
        """
        test function
        """
        if cmd == commands[0]:
            pass
        if cmd == commands[1]:
            return self.test_is_chrooted(output)

    def test_is_chrooted(self, output: str):
        """
        the server chrooted?
        if chrooted add a report!
        """

        report_type = "very suspicious"
        report_message = "this is very suspicious because the current directory is chrooted!"

        output = output.split(" ")
        if output[4] == "1000" and output[5] == "100":
            self.report_lists.append({"type": report_type, "message": report_message})


class CommandSender:
    def __init__(self, ssh_client: SSHClient, verbose:bool = False) -> None:
        self.ssh_client = ssh_client
        self.verbose = verbose
        transport = self.ssh_client.get_transport()
        self.channel = transport.open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()
        self.tester = Tester()
        
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

        server_msg = self.channel.recv(-1).decode()
        sleep(1)
        server_msg += self.channel.recv(-1).decode()
        return self.cut_the_useless_lines(server_msg, _from=0, usless_char="\r")

    @property
    def get_server_name(self) -> str:
        """
        get the name of server
        return: server_name
        """

        self.channel.send(" uname -a\n")
        sleep(1)
        return self.cut_the_useless_lines(self.channel.recv(-1).decode())

    def cut_the_useless_lines(self, output: str, _from: int = 1, _to:int = -1, usless_char: str = "\n") -> str:
        """
        cut the first line (your sned command)
        return: everything after first line
        """

        output = output.split(usless_char)[_from:_to]
        return "".join(output)

    def run(self):

        for cmd in commands:

            self.channel.send(cmd)
            sleep(5)
            stdout = self.channel.recv(-1).decode()
            if self.verbose:
                print(stdout)
            print(self.tester.test(cmd, self.cut_the_useless_lines(stdout)))

