textReplaceDict = {b"Stockholm":"Linköping",b"Smiley":"Trolly"}
linkReplaceDict = {b"/Stockholm-spring.jpg":"http://naturkartan-images.imgix.net/image/upload/jv1xkiprxn1fuvlg2amg/1408440053.jpg",b"smiley.jpg":"trolly.jpg"}

#Main function to try and modify request. 
def fake_request(headers):
    headers, foundLinksToReplace = replace_header(headers)
    request = reconstruct_headers(headers)
    host = headers[b"Host:"]
    return request, host, foundLinksToReplace

#Replaces header links by looking up the headertitle GET and Host and checking them against our two dictionaries textReplaceDict and linkReplaceDict.
def replace_header(headers):
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
def reconstruct_headers(headers):
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
def fake_response(headers,message):
    headers = dict(headers)
    message = bytes(message)

    dictionaryWordsInMessage = False
    for keys in textReplaceDict:
        if keys in message:
            dictionaryWordsInMessage = True

    if (dictionaryWordsInMessage == False):
        return headers, message,dictionaryWordsInMessage

    message = replace_message(message)
    
    contentLen = len(message)
    headers = change_len(headers,contentLen)
    
    return headers, message, dictionaryWordsInMessage

#Replaces the words in the text without changing the links in any <img/> html tag.
def replace_message(message):
    tagsIndexes = find_img_indexes(message)
    segments = segment_message(message,tagsIndexes)

    for key,value in textReplaceDict.items():
        counter = 0
        for seg in segments:
            if b"<img" not in seg:
                segments[counter] = seg.replace(key,value.encode())
            counter += 1
    message = reconstruct_message(segments)
    return message

#Reconstructs the message from the previously made segments.
def reconstruct_message(segments):
    message = b""
    for seg in segments:
        message +=seg
    
    return message

#Segments the message to allow us not to replace the text in any <img/> html tag.
def segment_message(message,tagsIndexes):
    messages = []
    
    if len(tagsIndexes) > 0:
        messages.append(message[0:tagsIndexes[0][0]])
        for i in range(len(tagsIndexes)):
            messages.append(message[tagsIndexes[i][0]:tagsIndexes[i][1]])
            if i+1 < len(tagsIndexes):
                messages.append(message[tagsIndexes[i][1]:tagsIndexes[i+1][0]])
        messages.append(message[tagsIndexes[len(tagsIndexes)-1][1]:-1])
    else:
        messages.append(message)
    return messages

#Finding the indexes of the <img/> html tags to be able to segment properly.
def find_img_indexes(message):
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
def change_len(headers,newlength):
    headers[b"Content-Length"] = str(newlength).encode()
    return headers 

#Checking if the content type is an image or not.
def check_content_type(headers):
    headers = dict(headers)
    if b"Content-Type:" in headers:
        contentType = get_content_type(headers)
        if b"text/html" not in contentType: 
            if b"image" in contentType:
                return False
    return True

#Extracts the header from the complete message. 
#This function is invoked when we receive data from our socket (The first iteration)
def parse_respons_to_header(message):
    index = message.find(b"\r\n\r\n")
    temp = message[0:index+4]
    if index == -1:
        return (temp,False)
    return (temp,True)

#Gets the content type
def get_content_type(headers):
    contentType = headers[b"Content-Type:"]
    return contentType


#Dividing up the request message into lines and then we create a dictionary
#that contains the header titles as a key and its information as its value.
def parse_header(request):
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

'''
    #Dividing up the request message into lines and then we create a dictionary
#that contains the header titles as a key and its information as its value.
def parse_header(request):
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
            value = b""
            for i in range(len(tmp)-1):
                value += tmp[i+1]              
            if len(tmp) > 0:
                temp[tmp[0]] = value
        
    return temp 
    '''