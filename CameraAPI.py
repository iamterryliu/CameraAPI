__author__ = 'Terry Liu # 2518'
import base64
import urllib2
from threading import Thread

import sys


def usage():
    print('Usage:')
    print('Default password is empty.')
    print('python CameraAPI.py [URL] [username] ')
    print('\nExample: $ python CameraAPI.py http://192.168.1.1/adm username \n')
    return


def basic_auth(host, username, password=''):
    try:
        request = urllib2.Request(host)
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        print("PASS: " + result.read())
    except urllib2.URLError, e:
        pass
    except Exception as e:
        pass


def main():
    if len(sys.argv) == 3:
        m_host = str(sys.argv[1])
        username = sys.argv[2]

        if len(username) == 0:
            print('The username cannot not empty.')
            exit()

        try:
            thread = Thread(target=basic_auth, args=(m_host, username,))
            thread.start()
            thread.join()
        except Exception as e:
            pass
    else:
        usage()


if __name__ == '__main__':
    main()
