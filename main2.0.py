# -*- coding: utf-8 -*

#---------- Include ----------

#---------- Variables Globals ----------
sizeW = 0
sizeH = 0
maxValueOfAByte = 0

MatrixesR = []
MatrixesG = []
MatrixesB = []

MatrixesY = []
MatrixesU = []
MatrixesV = []

matrixesYDivided = []
matrixesUDivided = []
matrixesVDivided = []
#---------- Function ----------
def getHeaderFile(fileOpened) :
    cpt = 0
    header = ''
    while cpt < 2 :
        header += fileOpened.read(1)
        if header[len(header)-1] == '\n' :
            cpt+=1
    return header
    
def getWidthSize(fileOpened) :
     sizeW = fileOpened.read(1)
     while sizeW[len(sizeW)-1] != ' ' :
         sizeW += fileOpened.read(1)           
     return int(sizeW)
    
def getHeigthSize(fileOpened) :
    sizeH = fileOpened.read(1)
    while sizeH[len(sizeH)-1] != '\n' :
        sizeH += fileOpened.read(1)
    return int(sizeH)

def getMaxValueOfAByte(fileOpened) :
    maxValueOfAByte = fileOpened.read(1)
    while maxValueOfAByte[len(maxValueOfAByte)-1] != '\n' :
        maxValueOfAByte += fileOpened.read(1)
    return int(maxValueOfAByte)

def getAllPixel(fileOpened) :
    global sizeW
    global sizeH
    global maxValueOfAByte
    tmpR = []
    tmpG = []
    tmpB = []
    
    for x in range (0,sizeH) :
        tmpR = []
        tmpG = []
        tmpB = []    
        
        for y in range (0,sizeW) :
            pixel = fileOpened.read(1)
            while pixel[len(pixel)-1] != '\n' :
                pixel += fileOpened.read(1)
            tmpR.append(int(pixel))

            pixel = fileOpened.read(1)
            while pixel[len(pixel)-1] != '\n' :
                pixel += fileOpened.read(1)
            tmpG.append(int(pixel))

            pixel = fileOpened.read(1)
            while pixel[len(pixel)-1] != '\n' :
                pixel += fileOpened.read(1)
            tmpB.append(int(pixel))
        
        MatrixesR.append(tmpR)
        MatrixesG.append(tmpG)
        MatrixesB.append(tmpB)    

    return    

def convertMatrixesToY() :
    for x in range (0,sizeH) :
        tmp = []
        for y in range (0,sizeW) :
            tmp.append(0.299 * MatrixesR[x][y] + 0.587 * MatrixesG[x][y] + 0.114 * MatrixesB[x][y])
        MatrixesY.append(tmp)    
    return 

def convertMatrixesToU() : 
    for x in range (0,sizeH) :
        tmp = []
        for y in range (0,sizeW) :
            tmp.append(128 - 0.1687*MatrixesR[x][y] - 0.3312*MatrixesG[x][y] + 0.5*MatrixesB[x][y])
        MatrixesU.append(tmp)    
    return

def convertMatrixesToV() : 
    for x in range (0,sizeH) :
        tmp = []
        for y in range (0,sizeW) :
            tmp.append(128 + 0.5*MatrixesR[x][y] - 0.4186*MatrixesG[x][y] + 0.0813*MatrixesB[x][y])
        MatrixesV.append(tmp)    
    return

def devideMatrixes(x,y,Matrixes) :
    tmp = [[0 for a in range(8)] for b in range(8)]
    for i in range(x,x+8) :
        for j in range(y,y+8) :
            tmp[i-x][j-y] = Matrixes[i][j]
    return tmp

def compressMatrixe(matrixesDivided) :
    for matrixes in matrixesDivided :
        for a in range(0,8,2) :
            for b in range(0,8,2) :
                valTmp = 0
                for i in range (a,a+2) :
                    for y in range (b,b+2) :
                        valTmp = valTmp + matrixes[i][y]    
                valTmp = valTmp / 4
                for i in range (a,a+2) :
                    for y in range (b,b+2) :
                        matrixes[i][y] = valTmp
    return 

def DiscreteCosineTransform() :
    for matrix in  matrixesYDivided :
        for values in matrix :
            for value in values :
                value = value - 128
    for matrix in  matrixesUDivided :
        for values in matrix :
            for value in values :
                value = value - 128
    for matrix in  matrixesVDivided :
        for values in matrix :
            for value in values :
                value = value - 128                         
    return 

#---------- Function Test ----------
def writeImgB(imgB,header,sizeW,sizeH,maxValueOfAByte) :
    imgB.write(header)
    imgB.write(str(sizeW)+" "+str(sizeH)+"\n")
    imgB.write(str(maxValueOfAByte)+"\n")
    print("Size of matrixesB : "+str(len(MatrixesB)))
    for x in MatrixesB :
        for y in x :
            imgB.write("0\n")
            imgB.write("0\n")
            imgB.write(str(y)+"\n")
    imgB.write("132\n")        
    return

def writeImgR(imgR,header,sizeW,sizeH,maxValueOfAByte) :
    imgR.write(header)
    imgR.write(str(sizeW)+" "+str(sizeH)+"\n")
    imgR.write(str(maxValueOfAByte)+"\n")
    print("Size of matrixesR : "+str(len(MatrixesR)))
    for x in MatrixesR :
        for y in x :
            imgR.write(str(y)+"\n")
            imgR.write("0\n")
            imgR.write("0\n")
    imgR.write("0\n")        
    return    

def writeImgG(imgG,header,sizeW,sizeH,maxValueOfAByte) :
    imgG.write(header)
    imgG.write(str(sizeW)+" "+str(sizeH)+"\n")
    imgG.write(str(maxValueOfAByte)+"\n")
    print("Size of matrixesG : "+str(len(MatrixesG)))
    for x in MatrixesG :
        for y in x :
            imgG.write("0\n")
            imgG.write(str(y)+"\n")
            imgG.write("0\n")
    imgG.write("0\n")        
    return

def writeImg(img,header,sizeW,sizeH,maxValueOfAByte) :
    img.write(header)
    img.write(str(sizeW)+" "+str(sizeH)+"\n")
    img.write(str(maxValueOfAByte)+"\n")
    print("Size of matrixes : "+str(len(MatrixesG[0])))
    print("Size of matrixes : "+str(len(MatrixesG[1])))
    print("Size of matrixes : "+str(len(MatrixesG[599])))
    for x in range(0,sizeH) :
        for y in range(0,sizeW) :
            img.write(str(MatrixesR[x][y])+"\n")
            img.write(str(MatrixesG[x][y])+"\n")
            img.write(str(MatrixesB[x][y])+"\n")          
    return   

#---------- Main ----------
fileBinary = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/nt-P3.ppm","rb")

print("Name : "+fileBinary.name)

# Recuperation of Head File
header = getHeaderFile(fileBinary)
print('Header : '+header)

# Recuperation of the Wide Size
sizeW = getWidthSize(fileBinary)
print('Witdh Size : '+str(sizeW))    

# Recuperation of the Heigth Size
sizeH = getHeigthSize(fileBinary)
print('Heigth Size : '+str(sizeH)) 

# Recuperation of the Heigth Size
maxValueOfAByte = getMaxValueOfAByte(fileBinary)
print('maxValueOfAByte : '+str(maxValueOfAByte))

# Fill all matrixes with the pixels
getAllPixel(fileBinary)

# Create Matrixe Y
convertMatrixesToY()
# Create Matrixe U
convertMatrixesToU()
# Create Matrixe V
convertMatrixesToV()

# Get All Matrixes Divided
for i in range(0,sizeH,8) :
    for j in range(0,sizeW,8) :
        matrixesYDivided.append(devideMatrixes(i,j,MatrixesY))
        matrixesUDivided.append(devideMatrixes(i,j,MatrixesU))
        matrixesVDivided.append(devideMatrixes(i,j,MatrixesV))

# Matrixes are Compress
compressMatrixe(matrixesUDivided)
compressMatrixe(matrixesVDivided)  

fileTest = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/test","wb")
fileTest.write(str(matrixesUDivided))

#---------- Code Test ----------

# imgB = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/imgB.ppm","wb")
# writeImgB(imgB,header,sizeW,sizeH,maxValueOfAByte)

# imgR = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/imgR.ppm","wb")
# writeImgR(imgR,header,sizeW,sizeH,maxValueOfAByte)

# imgG = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/imgG.ppm","wb")
# writeImgG(imgG,header,sizeW,sizeH,maxValueOfAByte)

# imgGlobal = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/imgGlob.ppm","wb")
# writeImg(imgGlobal,header,sizeW,sizeH,maxValueOfAByte)

# fileTest = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/test","wb")
# fileTest.write(str(matrixesYDivided))