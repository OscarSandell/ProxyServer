from email import header
from gettext import find


textReplaceDict = {"Stockholm":"Linköping","Smiley":"Trolly"}
linkReplaceDict = {"/Stockholm-spring.jpg":"https://www.glimstedt.se/wp-content/uploads/2016/04/Linkopingskontoret-600x600.jpg","smiley.jpg":"trolly.jpg"}

def parse_request(headers):
    print("Omodifierad Request: \n\n")
    GETHeader = str(headers["GET"])
    if GETHeader.find("smiley.jpg") != -1:
        headers["GET"] = GETHeader.replace("smiley.jpg",linkReplaceDict["smiley.jpg"])
    elif GETHeader.find("/Stockholm-spring.jpg") != -1:
        headers["GET"] = linkReplaceDict["/Stockholm-spring.jpg"]
        headers["Host"] = "glimstedt.se"
    '''
    for key,value in linkReplaceDict.items():
        for header in headers:
            headers[header] = headers[header].replace(key,value)
    '''
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

    index = sss.find("\r\n\r\n")
    headers = sss[0:index:1]
    print("Detta är response-headers")
    print(headers)
    print("Detta är gamla response \n\n\n\n\n\n")
    message = sss[index:len(sss)]
    print(message)

    imgIndexes = []
    imgIndexStart = 0
    while message.find("<img",imgIndexStart) != -1:
        if imgIndexStart == message.find("<img",imgIndexStart):
            break
        imgIndexStart = message.find("<img",imgIndexStart)
        imgIndexEnd = message.find(">",imgIndexStart)+1
        imgIndexes.append((imgIndexStart,imgIndexEnd))
        print("Start: {}; End: {}\n\n".format(imgIndexStart,imgIndexEnd))
        imgIndexStart = imgIndexEnd
    
    print("Här är våra <IMG> tags: \n\n {}".format(imgIndexes))
    '''''
    count = len(imgIndexes)
    currentCount = 0
    tmptext = ""
    for key,value in textReplaceDict.items():
        
        x = 0
        for start,end in imgIndexes.items():
            print("X: {}; start: {}\n".format(x,start))
            temp = message[x:start].replace(key,value)
            temp += message[start:end]
            x = end
            tmptext += temp
        currentCount += 1
        if currentCount == count:
            temp = message[x:-1].replace(key,value)
            tmptext += temp
        message = tmptext
    '''

    '''
    messages.append(messages[0:imgIndexes[0][0]])
    messages.append(messages[imgIndexes[0][1]:imgIndexes[1][0]])
    messages.append(messages[imgIndexes[1][1]:-1])
    '''
    messages = []
    if len(imgIndexes) > 0:
        
        messages.append(message[0:imgIndexes[0][0]])
        for i in range(len(imgIndexes)):
            print("\n\nDETTA ÄR FUCKING i:" + str(i) + "\n\n")
            if i+1 < len(imgIndexes):
                messages.append(message[imgIndexes[i][1]:imgIndexes[i+1][0]])
            messages.append(message[imgIndexes[i][0]:imgIndexes[i][1]])
        messages.append(message[imgIndexes[len(imgIndexes)-1][1]:-1])
        print("Detta är gammla message i en lista: {}\n\n".format(messages))
    
    for key,value in textReplaceDict.items():
        counter = 0
        for msg in messages:
            if "<img" not in msg:
                messages[counter] = msg.replace(key,value)
            counter += 1
    
    print("Detta är nya message i en lista: {}\n\n".format(messages))
    '''tmptext = ""
    for key,value in textReplaceDict.items():
        x = 0
        for start,end in imgIndexes.items():
            print("X: {}; start: {}\n".format(x,start))
            message[x:start] = message[x:start].replace(key,value)
            #temp += message[start:end]
            x = end
            #tmptext += temp
    '''
    message = ""
    for msg in messages:
        message +=msg
    print("Detta är nya parsade response \n\n\n\n\n")
    print(headers + message)
    #return headers,message
    return headers + message



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