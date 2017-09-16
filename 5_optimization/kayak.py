import time
import urllib2
import xml.dom.minidom

kayakkey = 'YOURKEYHERE'

def getkayaksession():
    # Construct the URL to start a session
    url = 'http://www.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey

    # Parse the resulting XML
    doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())

    # Find the <sid>xxxxxxxx</sid>
    sid = doc.getElementsByTagName('sid')[0].firstChild.data
    return sid

def flightsearch(sid, origin, destination, depart_date):
    # Construct search URL
    url='http://www.kayak.com/s/apisearch?basicmode=true&oneway=y&origin=%s' % origin
    url+='&destination=%s&depart_date=%s' % (destination,depart_date)
    url+='&return_date=none&depart_time=a&return_time=a'
    url+='&travelers=1&cabin=e&action=doFlights&apimode=1'
    url+='&_sid_=%s&version=1' % (sid)

    # Get the XML
    doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

    # Extract the search ID
    searchid=doc.getElementsByTagName('searchid')[0].firstChild.data

    return searchid
