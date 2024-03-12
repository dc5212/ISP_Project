#MY REFERENCE MONITOR


TYPE="type"
ARGS="args"
RETURN="return"
EXCP="exceptions"
TARGET="target"
FUNC="func"
OBJC="objc"

class ABFile():
  def __init__(self,filename,create):
    # global variables declaration is done here 
    
    mycontext['debug'] = False
    
    # I am giving local references to the file
    
    self.Afn = filename+'.a'
    self.Bfn = filename+'.b'

    #Now , I am Creating A/B Files
    if create:
      #First it checks if any backup files are present, if not it creates A/B Files and writes "SE" to A
      
      if self.Afn in listfiles():
        #If any backup File is present, it opens A/B File creates Original A,B Files, and then Empty B File
        self.Afile = openfile(self.Afn,create)
        self.Bfile = openfile(self.Bfn,create)
        self.Bfile.writeat(self.Afile.readat(None,0),0)
      else:
        self.Afile = openfile(self.Afn,create)
        self.Bfile = openfile(self.Bfn,create)
        self.Afile.writeat('SE', 0)
    else:
      #Now, check if Backup File Present, else raise an Exception
      if self.Afn in listfiles():
        self.Afile = openfile(self.Afn,True)
        self.Bfile = openfile(self.Bfn,True)
        self.Bfile.writeat(self.Afile.readat(None,0),0)
      else:
        raise FileNotFoundError

#WriteAt Function - Lock, Offset and Length Validation then Write the Data
#For Write Call, Lock provides better handling of multiple writes to a file
  def writeat(self,data,offset):
    #Creating the Lock
    self.lock = createlock()
    #Set the Lock to Blocking
    self.lock.acquire(True)
    #Offset Validation for Write Call
    if offset < 0:
        raise RepyArgumentError
        self.lock.release()
    elif offset > len(self.Bfile.readat(None,0)):
        raise SeekPastEndOfFileError
        self.lock.release()
    else:
      #After Correct Validation -> Write to File and Release Lock
      self.Bfile.writeat(data,offset)
      self.lock.release()

#ReadAt Function - Offset and Length Validation then Read & Return ReadData
  def readat(self,bytes,offset):
    #Creating the Lock
    self.lock = createlock()
    #Set the Lock to Blocking
    self.lock.acquire(True)
    #Offset and Length Validation for Read Call
    length = len(self.Afile.readat(None,0))
    if offset < 0 or length < 0:
      raise RepyArgumentError
      self.lock.release()
    elif offset >= len(self.Afile.readat(None,0)):
      raise SeekPastEndOfFileError
      self.lock.release()
    elif bytes > length and bytes != None:
      raise SeekPastEndOfFileError
      self.lock.release()
    elif (len(self.Afile.readat(None,0)) < offset+length) and bytes != None:
      raise RepyArgumentError
      self.lock.release()
    else:
      #Try Reading the File else raise Exception
      try:
         read_data = self.Afile.readat(bytes,offset)
         self.lock.release()
         return read_data
      except:
         raise RepyArgumentError

#Close Function Call - If both files are valid, older one is discarded else invalid file is discarded
  def close(self):
    #Data stored in variables for restoration of data
    backup_data = self.Afile.readat(None,0)
    data = self.Bfile.readat(None,0)
    backupfile = self.Afn
    #Check if the written file starts with "S" and ends with "E"
    if self.Bfile.readat(None,0).startswith("S") and self.Bfile.readat(None,0).endswith("E"):
      #The Written File is Valid -> Discard Older Version
      self.Afile.close()
      self.Bfile.close()
      removefile(self.Afn)
      openfile(backupfile,True).writeat(data,0)
      removefile(self.Bfn)
    else:
      #The Written File is Invalid -> Discard Invalid File
      self.Afile.close()
      self.Bfile.close()
      removefile(self.Afn)
      openfile(backupfile,True).writeat(backup_data,0)
      removefile(self.Bfn)

#Opens A/B Files if exist, else gives an Exception -> File Not Found
def ABopenfile(filename, create):
  return ABFile(filename,create)

# The code here sets up type checking and variable hiding for you.  You
# should not need to change anything below here.
sec_file_def = {"obj-type":ABFile,
                "name":"ABFile",
                "writeat":{"type":"func","args":(str,(int,long)),"exceptions":Exception,"return":(int,type(None)),"target":ABFile.writeat},
                "readat":{"type":"func","args":((int,long,type(None)),(int,long)),"exceptions":Exception,"return":str,"target":ABFile.readat},
                "close":{"type":"func","args":None,"exceptions":None,"return":(bool,type(None)),"target":ABFile.close}
           }

CHILD_CONTEXT_DEF["ABopenfile"] = {TYPE:OBJC,ARGS:(str,bool),EXCP:Exception,RETURN:sec_file_def,TARGET:ABopenfile}

# Execute the user code
secure_dispatch_module()