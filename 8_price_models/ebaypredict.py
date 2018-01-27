import httplib
from xml.dom.minidom import parse, parseString, Node

# devKey = '01b82a8b-8157-4879-ad28-6e61b33e2bc9'
appKey = 'BobbyLei-play-PRD-a5d705b3d-5455d325'
# certKey = 'PRD-5d705b3da941-dd34-48cd-b9a3-a612'
# userToken = 'AgAAAA**AQAAAA**aAAAAA**b5RsWg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6ADk4SmCJWGqQqdj6x9nY+seQ**KR8EAA**AAMAAA**M835DfdszUk0jci7RVknSVPJdrsrJUCI6m2/O3kIDAXCPEiQLpjlWLnEz+HyiigQL9BmsI2Vbk36ohbBHVW6sMoDMziY2fACMhPFnSKn1h4aCY6ShipGifvJbi/LJPCtKPbDjPms7kQsGVoM3J2eeYm8w3qEq3kRCjyCbRsbgOTR+/d0xfOiDQLnaG4VuW+shStB/tXzv5im2uDUlmrblDuMuEdSchJ02LCJXaMN6kNJaTYbzCtMxDYejfyYu2zuUhaQdqqmIfwwiZic97eW2MBxmnRuaLJk44StXxhf4vexv9lQoHoTCkfZzU6j4wq1laGqebLIwxjpufd6GJXwqC+2C35LK6WG4dHDLp0g3comaySWkySSYHks1QFQZUSadINaSvC71h9B56lH70Km1EcQvF8aeWoIjI+3/TDZhoXoR6a1KLw+xGWYKMnc/oV6ZMX8NVQ3hAWjL7wiuwSJPk9doKuufxuCIxcxAAg5x3RaR+mXssQLThm/AF765T6AmIeHU1pWoA4075pOGfVwZQniN5dTRRxACCymy3+lRd7FV/oPNXk0fhdKhXnHiKoeejj7f5lH0eYXWA1OOMn2bphmYrvGatY1X6G0d7BVXyUYFP432kH3VeW4KkBkmUvVwHU3/7e5ksrqLchlGeleqEX5QJ84FjHjbXT14jJL5geiU2o6QkIkd0M/JL7I3rrFjNSQJ5gPxh7n0FpD5sDT2y+2kYXhXrqTeUwoCECIs9nGcOGiNghbv/O80nWWwnp9'
serverUrl = 'svcs.ebay.com/services/search/FindingService/v1'


def getHeaders(apicall, siteID="0", compatabilityLevel="433"):
    headers = {
        "X-EBAY-SOA-SECURITY-APPNAME": appKey,
        "X-EBAY-SOA-OPERATION-NAME": apicall,
        "Content-Type": "text/xml"
    }
    return headers


def sendRequest(apicall, xmlparamters):
    connection = httplib.HTTPConnection(serverUrl)
    print "ABOUT TO"
    print xmlparamters
    print getHeaders(apicall)
    connection.request('POST', xmlparamters, getHeaders(apicall))
    print "ABOUT TO 2"
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
