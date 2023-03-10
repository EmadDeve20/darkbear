from typing import Dict, List
import re

from time import sleep
from paramiko import SSHClient, transport
from reporter import report

commands = [
    " apt search tmux\n",
    " ls -lia\n",
]

class Tester:
    """
    A Class With all of the Methods Test about whether the server is a honeypot or not!
    """
    report_lists:List[Dict] = []
    last_report:Dict = None
    def test(self, cmd: str, output: str):
        """
        test function
        """
        if cmd == commands[0]:
            self.test_packagemanager_is_ok(output)
        if cmd == commands[1]:
            return self.test_is_chrooted(output)

    def test_packagemanager_is_ok(self, output: str):
        """check the package manager is working or not"""        

        report_type = "suspicious"
        report_message = "this server does not have a package manager! maybe this is a not real Linux like cowrie"
        report = {"type": report_type, "message": report_message}

        not_found = re.search("^.*apt.*command not found", output)
        if not_found != None:
            self.report_lists.append(report)
            self.__append_to_last_report(report)

    def test_is_chrooted(self, output: str):
        """
        the server chrooted?
        if chrooted add a report!
        """

        report_type = "very suspicious"
        report_message = "this is very suspicious because the current directory is chrooted!"
        report = {"type": report_type, "message": report_message}

        output = output.split(" ")
        if output[4] == "1000" and output[5] == "100":
            self.report_lists.append(report)
            self.__append_to_last_report(report)

    def __append_to_last_report(self, report:Dict):
        self.last_report = report
    
    @property
    def get_last_report(self) -> Dict:
        """ return the last report and delete it for self """
        
        return self.last_report
        self.last_report = None

    def reporter(self) -> Dict:
        """yield any report"""
        for report in self.report_lists:
            yield report 
    
    @property
    def report_list_is_empty(self) -> bool:
        """return true if the length of report_lists is 0 if not, return the false"""
        return len(self.report_lists) == 0

    @property
    def have_a_suspicious_report(self) -> bool:
        """Do we have a suspicious report? return true if we have"""

        for r in self.report_lists:
            if r["type"] == "suspicious":
                return True
        return False

    @property
    def have_a_verysuspicious_report(self) -> bool:
        """Do we have a very suspicious report? return true if we have"""

        for r in self.report_lists:
            if r["type"] == "very suspicious":
                return True
        return False



class CommandSender:
    def __init__(self, ssh_client: SSHClient, verbose:bool = False, delay:int = 6, sync:bool = False,
                break_policy:str = None) -> None:
        self.ssh_client = ssh_client
        self.verbose = verbose
        self.delay = delay
        self.sync = sync
        self.break_policy = break_policy
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

        current_report_index = 0

        for cmd in commands:

            self.channel.send(cmd)
            sleep(self.delay)
            stdout = self.channel.recv(-1).decode()
            if self.verbose:
                print(stdout)
            self.tester.test(cmd, self.cut_the_useless_lines(stdout))

            if self.break_policy == "a" and not self.tester.report_list_is_empty:
                break

            if self.break_policy == "vs" and self.tester.have_a_verysuspicious_report:
                break

            if self.break_policy == "s" and self.tester.have_a_suspicious_report:
                break
            
            if self.sync and self.tester.report_lists[current_report_index] != None:
                print(f"current_report_index: {current_report_index}")
                report(self.tester.report_lists[current_report_index]["type"], 
                       self.tester.report_lists[current_report_index]["message"])


        if not self.tester.report_list_is_empty and not self.sync:
            for r in self.tester.reporter():
                report(r["type"], r["message"])

        elif self.tester.report_list_is_empty:
            report("not found", "No suspicious items were found")
