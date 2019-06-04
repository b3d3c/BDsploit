import subprocess

import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

# Get public SSH key
ssh_pub = config.get('exploit', 'ssh_pub')


'''
Function to delete SSH key
'''
def delSSH(rhost, privk_path):
    print("Deleting SSH key...")
    command = "grep -v \"" + ssh_pub + "\" /root/.ssh/authorized_keys > temp && mv -f temp /root/.ssh/authorized_keys"
    delssh = "ssh -o StrictHostKeyChecking=no -i " + privk_path + " root@" + rhost + " -t sh << \"EOF\"\n" + command + "\nEOF"
    subprocess.run(delssh, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


'''
Function to delete created user and all its files
'''
def delUser(rhost, privk_path):
    print("Deleting user...")
    command = "/usr/sbin/userdel -f test"
    delusr = "ssh -o StrictHostKeyChecking=no -i " + privk_path + " root@" + rhost + " -t sh << \"EOF\"\n" + command + "\nEOF"
    subprocess.run(delusr, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def delete(host, privk_path):
    delUser(host, privk_path)
    delSSH(host, privk_path)
