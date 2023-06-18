from typing import Dict

from time import sleep

from darkbear.test_models import test_models
from darkbear.commands import std_commands 
from darkbear.logger import std_suspicious_message
from darkbear.logger import logger


class TestChrooted(test_models.Tester):
    def __init__(self, os_name) -> None:
        super().__init__(command = std_commands.chroot_test_command,\
                        suspicious_message=std_suspicious_message.chrooted_test_suspicous_message,\
                          os_name = os_name)
    

    def test(self, ssh_chanel, delay:int = 3):
        
        ssh_chanel.send(self.command)
        sleep(delay)
        output_command = self.cut_the_useless_lines(self.channel.recv(-1).decode())

        output = output_command.split(" ")
        if output[4] == "1000" and output[5] == "100":
            logger.log(self.suspicious_message)
