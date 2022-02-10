textReplaceDict = {"Stockholm":"Linköping","Smiley":"Trolly"}
linkReplaceDict = {"/Stockholm-spring.jpg":"http://naturkartan-images.imgix.net/image/upload/jv1xkiprxn1fuvlg2amg/1408440053.jpg","smiley.jpg":"trolly.jpg"}

def parse_request(headers):
    #print("Omodifierad Request: \n\n")
    GETHeader = str(headers["GET"])
    if GETHeader.find("smiley.jpg") != -1:
        headers["GET"] = GETHeader.replace("smiley.jpg",linkReplaceDict["smiley.jpg"])
    elif GETHeader.find("/Stockholm-spring.jpg") != -1:
        #print(headers["GET"])
        headers["GET"] = linkReplaceDict["/Stockholm-spring.jpg"] + " HTTP/1.1"
        #print(headers["GET"])
        #print(headers["Host"])
        headers["Host"] = "naturkartan-images.imgix.net"
        #print(headers["Host"])

    request = ""
    for key,value in headers.items():
        if key == "GET":
            request += key + " " + value + "\r\n"
        elif key != "":
            request += key + ": " + value + "\r\n"
    request += "\r\n"
    return request

def parse_response(s):
    sss = str(s)
    print("\n\n\n\n\n", sss.encode(),"\n\n\n\n\n\n")
    index = sss.find("\r\n\r\n")
    headers = sss[0:index:1]
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

    print(message.encode())

    imgIndexes = []
    imgIndexStart = 0
    while message.find("<img",imgIndexStart) != -1:
        if imgIndexStart == message.find("<img",imgIndexStart):
            break
        imgIndexStart = message.find("<img",imgIndexStart)
        imgIndexEnd = message.find(">",imgIndexStart)+1
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
            if "<img" not in msg:
                messages[counter] = msg.replace(key,value)
            counter += 1
    
    print("Detta är nya message i en lista: {}\n\n".format(messages))

    message = ""
    for msg in messages:
        message +=msg
    contentLen = str(len(message.encode('UTF-8')))
    headers = change_len(headers,contentLen)
    print("Detta är nya parsade response \n\n\n\n\n")
    print(headers + message)
    return headers + message



def change_len(headers,int):
    headers = headers.split("\r\n")
    temp = {}
    for header in headers:
        if header.find("HTTP") != -1:
            tmp = header.split()
            value = ""
            for i in range(len(tmp)-1):
                value += tmp[i+1] + " "            
            if len(tmp) > 0:
                temp[tmp[0]] = value[:-1]
        else:
            tmp = header.split(": ")
            value = ""
            for i in range(len(tmp)-1):
                value += tmp[i+1]              
            if len(tmp) > 0:
                temp[tmp[0]] = value
    
    temp["Content-Length"] = int
    print("Nya headers: \n")
    print(temp)
    print("\n")
    
    string = ""
    for key,value in temp.items():
        if "HTTP" in key:
            string += key + " " + value + "\r\n"
        elif key != "":
            string += key + ": " + value + "\r\n"
    string += "\r\n"
    
    return string 
def add_fakenews():
    a = 1
    return a

def check_content_type(headers):
    print(headers)
    if "GET" in headers:
        if "Accept" in headers:
            if "text/html" not in headers["Accept"]: 
                if "image" in headers["Accept"]:
                    return False
    return True