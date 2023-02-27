from time import sleep
import argparse
import ssh_connection_manage

def pars_args():
    global host
    global port
    global known_hosts_file
    global username
    global password

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--host", type=str, help="Host to connect")
    arg_parser.add_argument("-p", "--port", type=int, default=22, help="Port")
    arg_parser.add_argument("-u", "--username", type=str, help="username")
    arg_parser.add_argument("-P", "--password", type=str, help="password")
    arg_parser.add_argument("-H", "--known-hosts", type=str, default="~/.ssh/known_hosts", help="the known_hosts file path")

    opt = arg_parser.parse_args()

    host = opt.host
    port = opt.port
    username = opt.username
    password = opt.password
    known_hosts_file = opt.known_hosts




if __name__ == "__main__":
    
    pars_args()
    ssh_connection = ssh_connection_manage.ssh_connect(host, port, username, password, known_hosts_file)
    print("Connect to server!")
    sleep(3)
    ssh_connection.close()

