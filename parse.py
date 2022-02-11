
textReplaceDict = {b"Stockholm":"Linköping",b"Smiley":"Trolly"}
linkReplaceDict = {b"/Stockholm-spring.jpg":"http://naturkartan-images.imgix.net/image/upload/jv1xkiprxn1fuvlg2amg/1408440053.jpg",b"smiley.jpg":"trolly.jpg"}

def parse_request(headers):
    headers = dict(headers)
    print("printar headers\n\n\n\n\n",headers)
    GETHeader = headers[b"GET"]
    if GETHeader.find(b"smiley.jpg") != -1:
        headers[b"GET"] = GETHeader.replace(b"smiley.jpg",linkReplaceDict[b"smiley.jpg"].encode())
    elif GETHeader.find(b"/Stockholm-spring.jpg") != -1:
        headers[b"GET"] = (linkReplaceDict[b"/Stockholm-spring.jpg"] + " HTTP/1.1").encode()
        headers[b"Host"] = b"naturkartan-images.imgix.net"

    request = b""
    for key,value in headers.items():
        if key == b"GET":
            request += key + b" " + value + b"\r\n"
        elif key != b"":
            request += key + b": " + value + b"\r\n"
    request += b"\r\n"
    return request

def parse_response(s):
    #sss = str(s)
    sss = s
    print("\n\n\n\n\n", sss,"\n\n\n\n\n\n")
    index = sss.find(b"\r\n\r\n")
    headers = sss[0:index]
    print("Detta är response-headers")
    print(headers)
    print("Detta är gamla response \n\n\n\n\n\n")
    message = sss[index:len(sss)]
    print(message)

    truth = False
    for keys in textReplaceDict:
        if keys in message:
            truth = True

    if truth == False:
        return headers + message

    print(message)

    imgIndexes = []
    imgIndexStart = 0
    while message.find(b"<img",imgIndexStart) != -1:
        if imgIndexStart == message.find(b"<img",imgIndexStart):
            break
        imgIndexStart = message.find(b"<img",imgIndexStart)
        imgIndexEnd = message.find(b">",imgIndexStart)+1
        if not (imgIndexEnd == imgIndexStart+1):
            imgIndexes.append((imgIndexStart,imgIndexEnd+1))
        print("Start: {}; End: {}\n\n".format(imgIndexStart,imgIndexEnd))
        imgIndexStart = imgIndexEnd
    
    print("Här är våra <IMG> tags: \n\n {}".format(imgIndexes))

    messages = []
    if len(imgIndexes) > 0:
        
        messages.append(message[0:imgIndexes[0][0]])
        for i in range(len(imgIndexes)):
            print("\n\nDETTA ÄR FUCKING i:" + str(i) + "\n\n")
            
            messages.append(message[imgIndexes[i][0]:imgIndexes[i][1]])
            if i+1 < len(imgIndexes):
                messages.append(message[imgIndexes[i][1]:imgIndexes[i+1][0]])
        messages.append(message[imgIndexes[len(imgIndexes)-1][1]:-1])
        print("Detta är gammla message i en lista: {}\n\n".format(messages))
    else:
        messages.append(message)
        
    for key,value in textReplaceDict.items():
        counter = 0
        for msg in messages:
            if b"<img" not in msg:
                messages[counter] = msg.replace(key,value.encode())
            counter += 1
    
    print("Detta är nya message i en lista: {}\n\n".format(messages))

    message = b""
    for msg in messages:
        message +=msg
    contentLen = len(message)
    headers = change_len(headers,contentLen)
    print("Detta är nya parsade response \n\n\n\n\n")
    print(headers + message)
    return headers + message



def change_len(headers,newlength):
    headers = headers.split(b"\r\n")
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
                temp[tmp[0]] = value
    
    temp[b"Content-Length"] = str(newlength).encode()
    print("Nya headers: \n")
    print(temp)
    print("\n")
    
    string = b""
    for key,value in temp.items():
        if b"HTTP" in key:
            string += key + b" " + value + b"\r\n"
        elif key != b"":
            string += key + b": " + value + b"\r\n"
    string += b"\r\n"
    
    return string 

def check_content_type(headers):
    print(headers)
    if "Content-Type" in headers:
        if "text/html" not in headers["Content-Type"]: 
            if "image" in headers["Content-Type"]:
                return False
        
    return True

def parse_respons_to_header(message):
    index = message.rfind(b"\r\n\r\n") +4 
    print(index)
    temp = message[0:index]
    return temp

def get_content_type(header):
    index = header.find(b'Content-Type: ')
    if index != -1:
        backslashr = header.find(b'\r',index)
        ContentType = header[index+14:backslashr]
    #ContentType = ContentType.decode()
    return ContentType

def check_content(headers):
    if b"image" in headers:
        return False
    else: 
        return True

def make_header_dir(request):
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


    '''if header.find("GET") != -1:
            tmp = header.split()
            value = ""
            for i in range(len(tmp)-1):
                value += tmp[i+1] + " "            
            if len(tmp) > 0:
                temp[tmp[0]] = value[:-1]
        elif header.find("HTTP") != -1:
            tmp = header.split()
            value = ""
            for i in range(len(tmp)-1):
                value += tmp[i+1] + " "            
            if len(tmp) > 0:
                temp[tmp[0]] = value[:-1]'''