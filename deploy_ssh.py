import sys
from time import sleep
import getpass
import paramiko
import re

from paramiko import AuthenticationException


class ShellHandler:

    def __init__(self, host, user, psw):
        self.ssh = paramiko.SSHClient()
        # BEWARE : UNSAFE
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, password=psw, port=22)

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def execute(self, cmd):
        """
        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                # up for now filled with shell junk from stdin
                shout = []
            elif str(line).startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap sherr with shout in a case of failure.
                    sherr = shout
                    shout = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        # first and last lines of shout/sherr contain a prompt
        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)

        return shin, shout, sherr


# simple padding on the output
def print_output(buff_out):
    for line in buff_out[0:-1]:
        val = line[0:-1]
        print(val)


# wrapper for paramiko execute command
def my_exec(_shell, cmd):
    _in, _out, _err = _shell.execute(cmd)
    print('shell@remote> ' + cmd)
    if not _err:
        print_output(_out)
    else:
        print('/!\ ERROR /!\ ')
        for line in _err[0:-1]:
            val = line[0:-1]
            print(val)
    print()



"""
User data to define manually
"""
PROJECT_NAME = 'catherinemathey'
GANDI_URL = 'd90e5820744144abb46bcbff3efd5424.testing-url.ws'
GANDI_USER = '2090221'
GANDI_GIT_REMOTE = 'git remote add gandiAuto git+ssh://2090221@git.sd6.gpaas.net/default.git'
GANDI_DEPLOY = 'ssh 2090221@git.sd6.gpaas.net deploy default.git'
GANDI_SSH = 'console.sd6.gpaas.net'
GANDI_DB_ROOT = 'hosting_db'

print()
GANDI_PSW = getpass.getpass(prompt='Gandi instance password: ')

print('connecting')

try:
    shell = ShellHandler('console.sd6.gpaas.net', '1832840', GANDI_PSW)
except paramiko.AuthenticationException as e:
    print("Oops!", sys.exc_info()[0], "occured. Re-trying")
    try:
        shell = ShellHandler('console.sd6.gpaas.net', '1832840', 'Geakxepo2!g')
    except paramiko.AuthenticationException as e:
        print("Oops!", sys.exc_info()[0], "occured again. Stopping script")
        exit()

print('connected. Waiting for shell opening')
sleep(6)
# my_exec(shell, '\r')
my_exec(shell, 'ls')
my_exec(shell, 'cd data')
my_exec(shell, 'ls')
shell.__del__()
