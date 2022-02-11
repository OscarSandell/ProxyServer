
from email.headerregistry import HeaderRegistry


textReplaceDict = {b"Stockholm":"Linköping",b"Smiley":"Trolly"}
linkReplaceDict = {b"/Stockholm-spring.jpg":"http://naturkartan-images.imgix.net/image/upload/jv1xkiprxn1fuvlg2amg/1408440053.jpg",b"smiley.jpg":"trolly.jpg"}

def fake_request(headers):
    headers = replace_header(headers)
    request = reconstruct_headers(headers)
    host = headers[b"Host:"]
    return request, host

def replace_header(headers):
    headers = dict(headers)
    ##print("#printar headers\n\n\n\n\n",headers)
    GETHeader = headers[b"GET"]
    if GETHeader.find(b"smiley.jpg") != -1:
        headers[b"GET"] = GETHeader.replace(b"smiley.jpg",linkReplaceDict[b"smiley.jpg"].encode())
    elif GETHeader.find(b"/Stockholm-spring.jpg") != -1:
        headers[b"GET"] = (linkReplaceDict[b"/Stockholm-spring.jpg"] + " HTTP/1.1").encode()
        headers[b"Host:"] = b"naturkartan-images.imgix.net"
    return headers

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

def fake_response(headers,message):
    headers = dict(headers)
    message = bytes(message)
    '''
    #print("\n\n\n\n\n", s,"\n\n\n\n\n\n")
    index = s.find(b"\r\n\r\n")
    headers = s[0:index]
    #print("Detta är response-headers")
    #print(headers)
    #print("Detta är gamla response \n\n\n\n\n\n")
    message = s[index:len(s)]
    #print(message)
    '''
    dictionaryWordsInMessage = False
    for keys in textReplaceDict:
        if keys in message:
            dictionaryWordsInMessage = True

    if (dictionaryWordsInMessage == False):
        #headers = reconstruct_headers(headers)
        return headers, message

    ##print(message)

    message = replace_message(message)
    

    contentLen = len(message)
    headers = change_len(headers,contentLen)
    
    
    
    
    ##print("Detta är nya message i en lista: {}\n\n".format(messages))

    
    ##print("Detta är nya parsade response \n\n\n\n\n")
    ##print(headers + message)
    return headers, message

def replace_message(message):
    tagsIndexes = find_img_indexes(message)
    segments = get_substrings(message,tagsIndexes)

    for key,value in textReplaceDict.items():
        counter = 0
        for seg in segments:
            if b"<img" not in seg:
                segments[counter] = seg.replace(key,value.encode())
            counter += 1
    message = reconstruct_message(segments)
    return message
    
def reconstruct_message(segments):
    message = b""
    for seg in segments:
        message +=seg
    
    return message
    
def get_substrings(message,tagsIndexes):
    messages = []
    
    if len(tagsIndexes) > 0:
        
        messages.append(message[0:tagsIndexes[0][0]])
        for i in range(len(tagsIndexes)):
            #print("\n\nDETTA ÄR FUCKING i:" + str(i) + "\n\n")
            
            messages.append(message[tagsIndexes[i][0]:tagsIndexes[i][1]])
            if i+1 < len(tagsIndexes):
                messages.append(message[tagsIndexes[i][1]:tagsIndexes[i+1][0]])
        messages.append(message[tagsIndexes[len(tagsIndexes)-1][1]:-1])
        #print("Detta är gammla message i en lista: {}\n\n".format(messages))
    else:
        messages.append(message)
    return messages
    
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
        #print("Start: {}; End: {}\n\n".format(imgIndexStart,imgIndexEnd))
        imgIndexStart = imgIndexEnd
    return imgIndexes

def change_len(headers,newlength):
    '''headers = headers.split(b"\r\n")
    temp = {}
    for header in headers:
        if header.find(b"HTTP") != -1:
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
                temp[tmp[0]] = value'''
    
    headers[b"Content-Length"] = str(newlength).encode()
    ##print("Nya headers: \n")
    ##print(    headers[b"Content-Length"] = str(newlength).encode())
    #print("\n")
    
    
    '''
    string = b""
    for key,value in temp.items():
        if b"HTTP" in key:
            string += key + b" " + value + b"\r\n"
        elif key != b"":
            string += key + b": " + value + b"\r\n"
    string += b"\r\n"
    '''
    
    return headers 

def check_content_type(headers):
    #print(headers)
    if "Content-Type" in headers:
        if "text/html" not in headers["Content-Type"]: 
            if "image" in headers["Content-Type"]:
                return False
        
    return True

def parse_respons_to_header(message):
    index = message.rfind(b"\r\n\r\n") +4 
    #print(index)
    temp = message[0:index]
    return temp

def get_content_type(headers):
    contentType = b""
    if b"Content-Type:" in headers:
        contentType = headers[b"Content-Type:"]
    return contentType

def check_content(contentType):
    if b"image" in contentType:
        return False
    else: 
        return True

def parse_header(request):
    headers = request.split(b"\r\n")
    #Delar upp headers i en dictionary med headernamn som nycklar
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