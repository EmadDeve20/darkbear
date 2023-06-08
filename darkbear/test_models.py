from typing import Dict, List
import re

from time import sleep
from paramiko import SSHClient, transport
from reporter import report
import output_messages

commands = [
    " apt search tmux\n", # package manager test TODO: this command must change for the current distribution
    " ls -lia\n", # chroot test
    " ifconfig || ip a\n", # check network mac address is for a virtual machine or not!
    " lsusb\n", # check if a USB name Like Virtual or VMware
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
        if cmd == commands[2]:
            self.test_it_is_a_virtual_machine_with_mac(output)
        if cmd == commands[3]:
            self.test_whether_usb_names_refer_to_virtual_or_not(output)

    def test_packagemanager_is_ok(self, output: str):
        """check the package manager is working or not"""        

        not_found = re.search("^.*apt.*command not found", output)
        if not_found != None:
            self.report_lists.append(output_messages.reports_types["package_manager_test"])
            self.__append_to_last_report(output_messages.reports_types["package_manager_test"])

    def test_is_chrooted(self, output: str):
        """
        the server chrooted?
        if chrooted add a report!
        """

        output = output.split(" ")
        if output[4] == "1000" and output[5] == "100":
            self.report_lists.append(output_messages.reports_types["chrooted_test"])
            self.__append_to_last_report(output_messages.reports_types["chrooted_test"])

    def test_it_is_a_virtual_machine_with_mac(self, output: str):

        vmware_mac_address_group = "(00:05:69:..:..:..|00:0C:29:..:..:..|00:50:56:..:..:..)"

        if re.match(f".*{vmware_mac_address_group}.*", output):
            self.report_lists.append(output_messages.reports_types["network_macaddress_test"])
            self.__append_to_last_report(output_messages.reports_types["network_macaddress_test"])
    
    def test_whether_usb_names_refer_to_virtual_or_not(self, output: str):

        if re.match(".*(Virtual|VMware).*", output, re.IGNORECASE):
            self.report_lists.append(output_messages.reports_types["usb_virtual_machine_test"])
            self.__append_to_last_report(output_messages.reports_types["usb_virtual_machine_test"])

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
        sleep(self.delay)
        server_msg += self.channel.recv(-1).decode()
        return self.cut_the_useless_lines(server_msg, _from=0, usless_char="\r")

    @property
    def get_server_name(self) -> str:
        """
        get the name of server
        return: server_name
        """

        self.channel.send(" uname -a\n")
        sleep(self.delay)
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
                       self.tester.report_lists[current_report_index]["description"])


        if not self.tester.report_list_is_empty and not self.sync:
            for r in self.tester.reporter():
                report(r["type"], r["description"])

        elif self.tester.report_list_is_empty:
            report("not found", "No suspicious items were found")
