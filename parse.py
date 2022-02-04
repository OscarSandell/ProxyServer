tabell = {"Stockholm-spring.jpg":"files/styles/max_1300x1300/public/linkopings_slotts-_och_domkyrkoomrade.jpg","Stockholm":"Linköping","Smiley":"Trolly","smiley.jpg":"trolly.jpg"}


def parse_response(s):
    sss = str(s)

    print("Vi printar här\n")
    index = sss.find("\r\n\r\n")
    headers = sss[0:index:1]
    print("Detta är headers")
    print(headers)
    print("Detta är gammla \n\n\n\n\n\n")
    message = sss[index:len(sss)]
    print(message)
    print("Nya \n\n\n\n\n")
    for key,value in tabell.items():
        message = message.replace(key,value)
    print(headers + message)
    #return headers,message
    return headers + message

def add_fakenews():
    a = 1
    return a

def check_content_type(headers):
    accept_header = headers[3].split()[1]
    print("\n\nACCAPT HEADER\n\n" + accept_header)
    if "text/html" in accept_header:
        return True
    return False