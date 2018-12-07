import os

def isAccess(path):
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False

def getPathHierrarhy(fullPath):
    pathes=[]
    currpath=""
    print(fullPath)
    if fullPath:
        for dir in fullPath[1:].split("/"):
            path=Path()
            path.dir=dir
            currpath+=dir+"/"
            path.hierrarhy=currpath
            pathes.append(path)
            pathes[-1].hierrarhy=pathes[-1].hierrarhy[0:-1]
        
        return pathes

def getPathHierrarhyFile(fullPath):
    pathes=[]
    currpath=""
    print(fullPath)
    if fullPath:
        for dir in fullPath[1:].split("/"):
            path=Path()
            path.dir=dir
            currpath+=dir+"/"
            path.hierrarhy=currpath
            pathes.append(path)
            pathes[-1].hierrarhy=pathes[-1].hierrarhy[0:-1]
        del pathes[-1]
        
        return pathes

class Path:
    dir=""
    hierrarhy=""