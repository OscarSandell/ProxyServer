tabell = {"Stockholm":"Linköping","Smiley":"Trolly"}

#,"smiley.jpg":"trolly.jpg"


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
    newstring = ""
    for key,value in tabell.items():
        message = message.replace(key,value)

    message = message.replace("UTF-8","hex")
    newstring = message
    print(newstring)
    #print(sss.encode())
    return newstring
    


    return s


#     if words in tabell:
#            message = message.replace(words,tabell[words])