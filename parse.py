textReplaceDict = {b"Stockholm":"Linköping",b"Smiley":"Trolly"}
linkReplaceDict = {b"/Stockholm-spring.jpg":"http://naturkartan-images.imgix.net/image/upload/jv1xkiprxn1fuvlg2amg/1408440053.jpg",b"smiley.jpg":"trolly.jpg"}

#Main function to try and modify request. 
#Pretty self explanatory :P
def FakeRequest(headers):
    headers, foundLinksToReplace = ReplaceHeader(headers)
    request = ReconstructHeader(headers)
    host = headers[b"Host:"]
    return request, host, foundLinksToReplace

#Replaces header links by looking up the headertitle GET and Host. Then it's checking them against
#our two dictionaries textReplaceDict and linkReplaceDict.
def ReplaceHeader(headers):
    headers = dict(headers)
    foundLinksToReplace = False
    GETHeader = headers[b"GET"]
    if GETHeader.find(b"smiley.jpg") != -1:
        headers[b"GET"] = GETHeader.replace(b"smiley.jpg",linkReplaceDict[b"smiley.jpg"].encode())
        foundLinksToReplace = True
    elif GETHeader.find(b"/Stockholm-spring.jpg") != -1:
        http = headers[b"GET"].split()
        headers[b"GET"] = (linkReplaceDict[b"/Stockholm-spring.jpg"] + " ").encode() + http[-1]
        headers[b"Host:"] = b"naturkartan-images.imgix.net"
        foundLinksToReplace = True
    return headers, foundLinksToReplace

#Reconstructs a bytestring from the headers dictionary.
#Goes through the headers dictionary and properly reconstructs it into a byte string.
def ReconstructHeader(headers):
    request = b""
    for key,value in headers.items():
        if key == b"GET":
            request += key + b" " + value + b"\r\n"
        elif b"HTTP" in key:
            request += key + b" " + value + b"\r\n"
        elif key != b"":
            request += key + b" " + value + b"\r\n"
    request += b"\r\n"
    return request

#Main function to replace the response and change content length if nessesary.
#First it checks if any of the keywords to replace are in the text, if notwe just return
#the headers, the message and a bool to tell the main loop that no changes has been made.
def FakeResponse(headers,message):
    headers = dict(headers)
    message = bytes(message)

    dictionaryWordsInMessage = False
    for keys in textReplaceDict:
        if keys in message:
            dictionaryWordsInMessage = True

    if (dictionaryWordsInMessage == False):
        return headers, message,dictionaryWordsInMessage

    message = ReplaceMessage(message)
    
    contentLen = len(message)
    headers = ChangeContentLength(headers,contentLen)
    
    return headers, message, dictionaryWordsInMessage

#Replaces the words in the text without changing the links in any <img/> html tag.
#It finds the index position of "<img>" in the message and then seperates the entire
#message into segments with "<img>" tags and segments without. It then goes through
#the segments and only replaces smiley and stockholm in the segments that does not
#contain this tag.
def ReplaceMessage(message):
    tagsIndices = FindImageIndices(message)
    segments = SegmentMessage(message,tagsIndices)

    for key,value in textReplaceDict.items():
        counter = 0
        for seg in segments:
            if b"<img" not in seg:
                segments[counter] = seg.replace(key,value.encode())
            counter += 1
    message = ReconstructMessage(segments)
    return message

#Reconstructs the message from the previously made segments.
def ReconstructMessage(segments):
    message = b""
    for seg in segments:
        message +=seg
    
    return message

#Segments the message to allow us not to replace the text in any <img/> html tag.
#We are seperating the text and messages into a list separately, for instance the list can look something 
#like this = ["smiley likes blalala","<img ./Stockholm />","something more texty Stockholm"].
#This is so that we can selectively replace the words we want inside the correct segment of the text.
def SegmentMessage(message,tagsIndices):
    segments = []
    
    if len(tagsIndices) > 0:
        segments.append(message[0:tagsIndices[0][0]])
        for i in range(len(tagsIndices)):
            segments.append(message[tagsIndices[i][0]:tagsIndices[i][1]])
            if i+1 < len(tagsIndices):
                segments.append(message[tagsIndices[i][1]:tagsIndices[i+1][0]])
        segments.append(message[tagsIndices[len(tagsIndices)-1][1]:-1])
    else:
        segments.append(message)
    return segments

#This function will execute if we find any of our keywords to replace in the response
#In this function we are finding the indices of the <img/> html tags to be able to separate the tags 
#from the plain text so that we can replace the words to replace with the decired elements.
def FindImageIndices(message):
    imgIndexes = []
    imgIndexStart = 0
    while message.find(b"<img",imgIndexStart) != -1:
        if imgIndexStart == message.find(b"<img",imgIndexStart):
            break
        imgIndexStart = message.find(b"<img",imgIndexStart)
        imgIndexEnd = message.find(b">",imgIndexStart)+1
        if not (imgIndexEnd == imgIndexStart+1):
            imgIndexes.append((imgIndexStart,imgIndexEnd+1))
        imgIndexStart = imgIndexEnd
    return imgIndexes

#Change information in the Content-Length headertitle.
def ChangeContentLength(headers,newlength):
    headers[b"Content-Length"] = str(newlength).encode()
    return headers 

#Checking if the content type is an image or not by grabbing the 
#Content-Type header from the headers dictionary and checking its
#value.
def CheckContentType(headers):
    headers = dict(headers)
    if b"Content-Type:" in headers:
        contentType = GetContentType(headers)
        if b"text/html" not in contentType: 
            if b"image" in contentType:
                return False
    return True

#Extracts the header from the complete message. 
#This function is invoked when we receive data from our socket (most likely the first iteration) and it returns temp
def ParseResponseToHeaders(message):
    index = message.find(b"\r\n\r\n")
    temp = message[0:index+4]
    if index == -1:
        return (temp,False)
    return (temp,True)

#Gets the content type
def GetContentType(headers):
    contentType = headers[b"Content-Type:"]
    return contentType


#Dividing up the request message into lines and then we create a dictionary
#that contains the header titles as a key and its information as its value.
def ParseHeader(request):
    headers = request.split(b"\r\n")
    temp = {}
    for header in headers:
        if b'GET' or b'HTTP' in header:
            tmp = header.split()
            value = b""
            for i in range(len(tmp)-1):
                value += tmp[i+1] + b" "            
            if len(tmp) > 0:
                temp[tmp[0]] = value[:-1]
        else:
            tmp = header.split(b": ")
            temp[tmp[0]] = tmp[1]
        
    return temp 