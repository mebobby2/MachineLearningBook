from akismet import Akismet

defaultkey = "cc36a6531592"
pageurl = "http://yoururlhere.com"

defaultagent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.7) "
defaultagent += "Gecko/20060909 Firefox/1.5.0.7"

def isspam(comment, author, ipaddress, agent = defaultagent, apikey = defaultkey):
    try:
        api = Akismet(apikey, pageurl)
        valid = api.verify_key()
        if valid:
            return api.comment_check(comment, { 'user_ip': ipaddress, 'user_agent': 'Example/0.1', 'comment_author_email': author })
        else:
            print 'Invalid key'
            return False
    except akismet.AkismetError, e:
        print e
        return False

