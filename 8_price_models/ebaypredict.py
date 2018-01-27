import httplib
from xml.dom.minidom import parse, parseString, Node

appKey = 'BobbyLei-play-PRD-a5d705b3d-5455d325'
serverUrl = 'svcs.ebay.com'


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
    print 'Results' + data
    response = parseString(data)
    itemNodes = response.getElementsByTagName('Item')
    results = []
    for item in itemNodes:
        itemId = getSingleValue(item, 'ItemID')
        itemTitle = getSingleValue(item, 'Title')
        itemPrice = getSingleValue(item, 'CurrentPrice')
        itemEnds = getSingleValue(item, 'EndTime')
        results.append((itemId, itemTitle, itemPrice, itemEnds))
    return results


def getCategory(query='', parentID=None, siteID='0'):
    lquery = query.lower()
    xml = "<?xml version='1.0' encoding='utf-8'?>" +\
        "<GetCategoriesRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">" +\
        "<RequesterCredentials><eBayAuthToken>" +\
        userToken +\
        "</eBayAuthToken></RequesterCredentials>" +\
        "<DetailLevel>ReturnAll</DetailLevel>" +\
        "<ViewAllNodes>true</ViewAllNodes>" +\
        "<CategorySiteID>" + siteID + "</CategorySiteID>"
    if parentID == None:
        xml += "<LevelLimit>1</LevelLimit>"
    else:
        xml += "<CategoryParent>" + str(parentID) + "</CategoryParent>"
    xml += "</GetCategoriesRequest>"
    data = sendRequest('GetCategories', xml)
    categoryList = parseString(data)
    catNodes = categoryList.getElementsByTagName('Category')
    for node in catNodes:
        catid = getSingleValue(node, 'CategoryID')
        name = getSingleValue(node, 'CategoryName')
        if name.lower().find(lquery) != -1:
            print catid, name
