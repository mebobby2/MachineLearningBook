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
        if tagNode.hasChildNodes():
            return tagNode.firstChild.nodeValue
    return ''


def callid():
    return str(int(time.time() * 10))

# import facebook
# s=facebook.fbsession()
# friends=s.getfriends()

class fbsession():
    def __init__(self):
        self.session_secret = None
        self.session_key = None
        self.token = self.createtoken()
        webbrowser.open(self.getlogin())
        print "Press enter after logging in:", raw_input()
        self.getsession()

    def getfriends(self):
        doc = self.sendrequest({'method': 'facebook.friends.get',
                                'session_key': self.session_key,
                                'call_id': callid()})
        results = []
        for n in doc.getElementsByTagName('result_elt'):
            results.append(n.firstChild.nodeValue)
        return results

    def getinfo(self, users):
        ulist = ','.join(users)

        fields = 'gender,current_location,relationship_status,' +\
            'affiliations,hometown_location'

        doc = self.sendrequest({'method': 'facebook.users.getInfo', 'session_key': self.session_key,
                                'call_id': callid(), 'users': ulist, 'fields': fields})

        results = {}
        for n, id in zip(doc.getElementsByTagName('result_elt'), users):
                # Get the location
                locnode = n.getElementsByTagName('hometown_location')[0]
                loc = getsinglevalue(locnode, 'city')+', ' + \
                                    getsinglevalue(locnode, 'state')
                # Get school
                college = ''
                gradyear = '0'
                affiliations = n.getElementsByTagName('affiliations_elt')
                for aff in affiliations:
                    # Type 1 is college
                    if getsinglevalue(aff, 'type') == '1':
                        college = getsinglevalue(aff, 'name')
                        gradyear = getsinglevalue(aff, 'year')
                results[id] = {'gender': getsinglevalue(n, 'gender'),
                            'status': getsinglevalue(n, 'relationship_status'),
                            'location': loc, 'college': college, 'year': gradyear}
        return results

    def sendrequest(self, args):
        args['api_key'] = apiKey
        args['sig'] = self.makehash(args)
        post_data = urllib.urlencode(args)
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
