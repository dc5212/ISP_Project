if "testfile.txt.a" in listfiles():
    removefile("testfile.txt.a")

if "testfile.txt.b" in listfiles():
    removefile("testfile.txt.b")

myfile=ABopenfile("testfile.txt",True)
myfile.writeat("SaaaaaE",0)
myfile.close()

myfile=ABopenfile("testfile.txt",True)
myfile.writeat("ssssE",7)
myfile.close()

myfile=ABopenfile("testfile.txt",True)

try:
    assert('SaaaaaEssssE' == myfile.readat(None,0))
    myfile.close()

except:
    myfile.close()
    log("Data entry error! \n")

finally:
    exitall()