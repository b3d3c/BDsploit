import shodan
import sys
import configparser
import requests
import threading
import queue


config = configparser.ConfigParser()
config.read('conf.ini')

# Get testing value
test = config.getboolean('shodan', 'test')

if test:
    test_url = config.get('shodan', 'test_url')

# Get Shodan API key
SHODAN_API_KEY = config.get('shodan', 'key')
api = shodan.Shodan(SHODAN_API_KEY)

# Get number of threads to use
NUMT = config.get('shodan', 'NUMT')

q = queue.Queue()
san = queue.Queue()


'''
Search results using Shodan API
'''
def search():
    try:
        results = api.search('X-Marathon-Leader')
        for result in results['matches']:
            try:
                ip = result['http']['host']
                ip_str = result['ip_str']
                if ip != ip_str:
                    ip = ip_str
                port = str(result['port'])
                loc = result['http']['location']
                if port == '443':
                    url = 'https://' + ip + loc
                elif port == '8443':
                    url = 'https://' + ip + ':' + port + loc
                else:
                    url = 'http://' + ip + ':' + port + loc
                q.put(url)
            except KeyError:
                continue

    except shodan.APIError as e:
            print('Error: {}'.format(e))


'''
Sanitize list, remove not 200 OK URLs
'''
def sanitize():
    url = q.get()
    try:
        status = requests.get(url, timeout=5, verify=False).status_code
        if status == 200:
            san.put(url)
    except (requests.ConnectTimeout, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        return


'''
Producer work
'''
def producer():
    try:
        search()
    except (OSError, KeyboardInterrupt):
        sys.exit(0)


'''
Consumer work
'''
def consumer():
    while not q.empty():
        sanitize()


'''
Start threads function
'''
def startThreads():
    p = threading.Thread(target=producer)
    consumers = [threading.Thread(target = consumer) for i in range(int(NUMT))]

    p.daemon = True
    p.start()
    p.join()
    for c in consumers:
        c.daemon = True
        c.start()
    for c in consumers:
        c.join()


def start():
    if test:
        return [test_url]
    startThreads()
    l = []
    while not san.empty():
        v = san.get()
        l.append(v)
