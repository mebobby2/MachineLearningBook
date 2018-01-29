import httplib
from xml.dom.minidom import parse, parseString, Node

appKey = 'BobbyLei-play-PRD-a5d705b3d-5455d325'
serverUrl = 'svcs.ebay.com'

# import ebaypredict
# import oldebayapi
# oldebayapi.getCategory('computers')
# oldebayapi.getCategory('laptops',parentID=58058)
# laptops=ebaypredict.doSearch('laptop',categoryID=51148)
# oldebayapi.getItem(laptops[7][0])

def getHeaders(apicall, siteID="0", compatabilityLevel="433"):
    headers = {
        "X-EBAY-SOA-SECURITY-APPNAME": appKey,
        "X-EBAY-SOA-OPERATION-NAME": apicall,
        "Content-Type": "application/xml"
    }
    return headers


def sendRequest(apicall, xmlparamters):
    connection = httplib.HTTPConnection(serverUrl)
    connection.request('POST', '/services/search/FindingService/v1', xmlparamters, getHeaders(apicall))
    response = connection.getresponse()
    if response.status != 200:
        print "Error sending request: " + response.reason
    else:
        data = response.read()
        connection.close()
    return data


def getSingleValue(node, tag):
    nl = node.getElementsByTagName(tag)
    if len(nl) > 0:
        tagNode = nl[0]
        if tagNode.hasChildNodes():
            return tagNode.firstChild.nodeValue
    return '-1'

# New eBay API: http://developer.ebay.com/devzone/finding/concepts/MakingACall.html
def doSearch(query, categoryID=None, page=1):
    xml = "<?xml version='1.0' encoding='utf-8'?>" +\
        "<findItemsAdvancedRequest xmlns=\"http://www.ebay.com/marketplace/search/v1/services\">" +\
        "<paginationInput>" +\
            "<entriesPerPage>200</entriesPerPage>" +\
            "<pageNumber>" + str(page) + "</pageNumber>" +\
        "</paginationInput>" +\
        "<keywords>" + query + "</keywords>"
    if categoryID != None:
        xml += "<categoryId>" + str(categoryID) + "</categoryId>"
    xml += "</findItemsAdvancedRequest>"

    data = sendRequest('findItemsAdvanced', xml)
    response = parseString(data)
    itemNodes = response.getElementsByTagName('item')
    results = []
    for item in itemNodes:
        itemId = getSingleValue(item, 'itemId')
        itemTitle = getSingleValue(item, 'title')
        itemPrice = getSingleValue(item, 'currentPrice')
        itemEnds = getSingleValue(item, 'endTime')
        results.append((itemId, itemTitle, itemPrice, itemEnds))
    return results
