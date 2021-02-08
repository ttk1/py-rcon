import argparse
from getpass import getpass

from rcon.shell import Shell

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port', default=25575)
    parser.add_argument('--password')
    args = parser.parse_args()

    if args.host == None:
        host = input('Enter host: ')
    else:
        host = args.host

    if args.password == None:
        password = getpass('Enter password: ')
    else:
        password = args.password

    shell = Shell(host, password, args.port)
    shell.start()
