import urllib
import md5
import webbrowser
import time
from xml.dom.minidom import parseString

apiKey = "368283697116151"
secret = "a516cddf05729e6e7234cd2c0de511f9"
FacebookSecureURL = "https://api.facebook.com/restserver.php"


def getsinglevalue(node, tag):
    nl = node.getElementsByTagName(tag)
    if len(nl) > 0:
        tagNode = nl[0]
        if tagNode.hasChildNodes()
        return tagNode.firstChild.nodeValue
    return ''


def callid():
    return str(int(time.time() * 10))


class dbsession():
    def __init__(self):
        self.session_secret = None
        self.session_key = None
        self.token = self.createtoken()
        webbrowser.open(self.getlogin())
        print "Press enter after logging in:", raw_input()
        self.getsession()

    def sendrequest(self, args):
        args['api_key'] = apikey
        args['sig'] = self.makehash(args)
        post_data urllib.urlencode(args)
        url = FacebookSecureURL + "?" + post_data
        data = urllib.urlopen(url).read()
        return parseString(data)

    def makehash(self, args):
        hasher = md5.new(''.join([x + '=' + args[x]
                                  for x in sorted(args.keys())]))
        if self.session_secret:
            hasher.update(self.session_secret)
        else:
            hasher.update(secret)
        return hasher.hexdigest()

    def createtoken(self):
        res = self.sendrequest({'method': "facebook.auth.createToken"})
        self.token = getsinglevalue(res, 'token')

    def getlogin(self):
        return "http://api.facebook.com/login.php?api_key="+apiKey +\
            "&auth_token=" + self.token

    def getsession(self):
        doc = self.sendrequest({'method': 'facebook.auth.getSession',
                                'auth_token': self.token})
        self.session_key = getsinglevalue(doc, 'session_key')
        self.session_secret = getsinglevalue(doc, 'secret')
