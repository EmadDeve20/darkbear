import argparse
import ssh_connection_manage
from test_models import CommandSender
from sys import argv
from paramiko.ssh_exception import NoValidConnectionsError

def help():
    print("Usage: ")
    print("--host IP address of server")
    print("-p or --port port of server default=22")
    print("-u or --username username")
    print("-P or --password password")
    print("-H or --known-hosts public key file default=~/.ssh/known_hosts")
    print("-h or --help Help")
    print("--verbose do print all of commands and outputs")
    print("-d [number] or --delay [number] delay receiving after sending a command default = 6")
    print("the delay must be greater than 6!")
    print("-s or --sync", end=" ")
    print("The sync argument makes it pass the suspicious item as soon as it sees it and does not wait until the last test method")
    print("-b or --break-policy for break policy")
    print("the policy of breaking script when found a something suspicious [a|s|vs]", end=" ")
    print("a = any s = suspicious vs = very suspicious")

def pars_args():
    global host
    global port
    global known_hosts_file
    global username
    global password
    global verbose
    global delay
    global sync
    global break_policy

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--host", type=str, help="Host to connect")
    arg_parser.add_argument("-p", "--port", type=int, default=22, help="Port")
    arg_parser.add_argument("-u", "--username", type=str, help="username")
    arg_parser.add_argument("-P", "--password", type=str, help="password")
    arg_parser.add_argument("-H", "--known-hosts", type=str, default="~/.ssh/known_hosts", help="the known_hosts file path")
    arg_parser.add_argument("--verbose", action="store_true", default=False, help="print all of commands and outputs")
    arg_parser.add_argument("-d", "--delay", type=int, default=6, help="delay receiving after sending a command default = 6")
    arg_parser.add_argument("-s", "--sync", action="store_true", default=False, help="As soon as you see something suspicious, display it")
    arg_parser.add_argument("-b", "--break-policy", choices=["a", "s", "vs"], default=None, help="the policy of breaking script when found something suspicious [a|s|vs]")

    opt = arg_parser.parse_args()

    host = opt.host
    port = opt.port
    username = opt.username
    password = opt.password
    known_hosts_file = opt.known_hosts
    verbose = opt.verbose
    delay = opt.delay
    sync = opt.sync
    break_policy = opt.break_policy

    if (delay < 6):
        print("the delay must be greater than 6!")
        exit(1)

def run():

    pars_args()

    if len(argv) == 1:
        help()
        exit(1)

    try:
        ssh_connection = ssh_connection_manage.ssh_connect(host, port, username, password, known_hosts_file)
        print("Connect to server!")
    except NoValidConnectionsError as err:
        print(err.strerror)
        exit(1)

    
    command_sender =  CommandSender(ssh_connection, verbose, delay, sync, break_policy)
    
    try:
        command_sender.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run()
    
