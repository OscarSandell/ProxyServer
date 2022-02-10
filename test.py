textReplaceDict = {"Stockholm":"Linköping","Smiley":"Trolly"}
#linkReplaceDict = {"/Stockholm-spring.jpg":"https://www.glimstedt.se/wp-content/uploads/2016/04/Linkopingskontoret-600x600.jpg","smiley.jpg":"trolly.jpg"}
linkReplaceDict = {"/Stockholm-spring.jpg":"http://www.columbia.edu/~fdc/picture-of-something.jpg","smiley.jpg":"trolly.jpg"}

lkpg = "Linköping"
sthlm = "Stockholm"
smil = "Smiley"
trol = "Trolly"

print("Storleken av Linköping vs Stockholm = {} vs {} bytes".format(len(lkpg.encode('UTF-8')),len(sthlm.encode('UTF-8'))))

print("Storleken av Smiley vs Trolly = {} vs {} bytes".format(len(smil.encode('UTF-8')),len(trol.encode('UTF-8'))))