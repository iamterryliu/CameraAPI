__author__ = 'Terry Liu # 2518'
import base64
import sys
import urllib2
from threading import Thread


def usage():
    logger.debug('Usage:')
    logger.debug('Default password is empty.')
    logger.debug('python CameraAPI.py [URL] [username] ')
    logger.debug('\nExample: $ python CameraAPI.py http://192.168.1.1/adm username \n')
    return


def basic_auth(host, username, password=''):
    try:
        request = urllib2.Request(host)
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        logger.debug(result.read())
    except urllib2.URLError, e:
        logger.debug(e.reason)
        pass


def main():
    if len(sys.argv) == 3:
        m_host = str(sys.argv[1])
        username = sys.argv[2]
        # password = sys.argv[-1]

        # logger.debug('m_host=' + m_host)
        # logger.debug('username=' + username)
        # logger.debug('password=' + password)

        if len(username) == 0:
            logger.debug('The username cannot not empty.')
            exit()

        thread = Thread(target=basic_auth, args=(m_host, username,))
        thread.start()
        thread.join()

    else:
        usage()


if __name__ == '__main__':
    main()
