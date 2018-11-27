# -*- coding: utf-8 -*

#---------- Include ----------
from math import *
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

matrixesYDecompressed = []
matrixesUDecompressed = []
matrixesVDecompressed = []

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
            tmpValue = (0.257 * MatrixesR[x][y]) + (0.504 * MatrixesG[x][y]) + (0.098 * MatrixesB[x][y]) + 16.0
            if(tmpValue > 255) :
                tmpValue = 255
            if(tmpValue < 0) :
                tmpValue = 0
            tmp.append(tmpValue)
        MatrixesY.append(tmp)    
    return 

def convertMatrixesToU() : 
    for x in range (0,sizeH) :
        tmp = []
        for y in range (0,sizeW) :
            tmpValue = (-(0.148 * MatrixesR[x][y])) - (0.291 * MatrixesG[x][y]) + (0.439 * MatrixesB[x][y]) + 128.0
            if(tmpValue > 255) :
                tmpValue = 255
            if(tmpValue < 0) :
                tmpValue = 0
            tmp.append(tmpValue)
        MatrixesU.append(tmp)    
    return

def convertMatrixesToV() : 
    for x in range (0,sizeH) :
        tmp = []
        for y in range (0,sizeW) :
            tmpValue = (0.439*MatrixesR[x][y]) - (0.368*MatrixesG[x][y]) - (0.071*MatrixesB[x][y]) + 128
            if(tmpValue > 255) :
                tmpValue = 255
            if(tmpValue < 0) :
                tmpValue = 0
            tmp.append(tmpValue)
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

def decompressMatrixes(matrixes) :
    matrixesDecompressed = []
    cpt = 0
    for notUsed in range(0,75) :
        for line in range (0,8) : 
            for matrix in range(cpt+0,cpt+100) :
                for value in range(0,8) :
                    matrixesDecompressed.append(matrixes[matrix][line][value])
        cpt = cpt + 100
    return matrixesDecompressed       


def DiscreteCosineTransform(matrixeY,matrixeU,matrixeV) :
    for matrix in range(0,len(matrixeY)) :
        for lines in range(0,len(matrixeY[matrix])) :
            for value in range(0,len(matrixeY[matrix][lines])) :
                matrixeY[matrix][lines][value] = matrixeY[matrix][lines][value] - 128
    for matrix in range(0,len(matrixeU)) :
        for lines in range(0,len(matrixeU[matrix])) :
            for value in range(0,len(matrixeU[matrix][lines])) :
                matrixeU[matrix][lines][value] = matrixeU[matrix][lines][value] - 128
    for matrix in range(0,len(matrixeV)) :
        for lines in range(0,len(matrixeV[matrix])) :
            for value in range(0,len(matrixeV[matrix][lines])) :
                matrixeV[matrix][lines][value] = matrixeV[matrix][lines][value] - 128         
    return

def InverseDiscreteCosineTransform(matrixeY,matrixeU,matrixeV) :
    for matrix in range(0,len(matrixeY)) :
        for lines in range(0,len(matrixeY[matrix])) :
            for value in range(0,len(matrixeY[matrix][lines])) :
                matrixeY[matrix][lines][value] = matrixeY[matrix][lines][value] + 128
    for matrix in range(0,len(matrixeU)) :
        for lines in range(0,len(matrixeU[matrix])) :
            for value in range(0,len(matrixeU[matrix][lines])) :
                matrixeU[matrix][lines][value] = matrixeU[matrix][lines][value] + 128
    for matrix in range(0,len(matrixeV)) :
        for lines in range(0,len(matrixeV[matrix])) :
            for value in range(0,len(matrixeV[matrix][lines])) :
                matrixeV[matrix][lines][value] = matrixeV[matrix][lines][value] + 128         
    return    

def ForwardDCT(matrixesDivided) :
    matrix = []
    for cpt in range(0,len(matrixesDivided)) :
        tabTmp = [[0 for a in range(8)] for b in range(8)]
        for v in range(0,8) :
            for u in range(0,8) :
                # Calcul of DCT coef
                if u == 0 :
                    U = 1.0 / sqrt(2)
                    V = 1.0 / sqrt(2)
                else :
                    U = 1.0    
                    V = 1.0
                coef = (U*V)/4
                tmp = 0
                for y in range(0,8) :
                    for x in range(0,8) :
                        # Use classe's fonction 
                        # tmp = tmp + matrixesDivided[cpt][x][y]*cos(((2*x+1)*u*pi)/16)*cos(((2*y+1)*v*pi)/16)
                        tmp = tmp + cos(((2*x+1)*u*pi)/16)*cos(((2*y+1)*v*pi)/16)
                tmp = tmp * coef
                # Add value in matrix UV
                tabTmp[v][u] = tmp
        # Add matrixes in main tab
        matrix.append(tabTmp)        
    return matrix

def InverseDCT (matrixDCT) :
    matrix = []
    for cpt in range(0,len(matrixDCT)) :
        tabTmp = [[0 for a in range(8)] for b in range(8)]
        for x in range(0,8) :
            for y in range(0,8) :
                # Calcul of DCT coef
                tmp = 0
                for u in range(0,8) :
                    for v in range(0,8) :
                        if u == 0 :
                            U = 1.0 / sqrt(2)
                            V = 1.0 / sqrt(2)
                        else :
                            U = 1.0    
                            V = 1.0
                        coef = U*V
                        # Use classe's fonction 
                        tmp = tmp + coef * matrixDCT[cpt][u][v] * cos(((2*x+1)*u*pi)/16) * cos(((2*y+1)*v*pi)/16)
                tmp = tmp * 0.25
                # Add value in matrix UV
                tabTmp[x][y] = tmp
        # Add matrixes in main tab
        matrix.append(tabTmp)        
    return matrix

def createQuantizer(integer) :
    tab = []
    for i in range (0,((sizeH*sizeW)/8)/8) :
        tabTmp = [[integer for a in range(8)] for b in range(8)]
        tab.append(tabTmp)
    return tab

def quantizedMatrix(matrix,quantizer) :
    tab = []
    for i in range (0,len(matrix)) :
        tabTmp = [[0 for a in range(8)] for b in range(8)]
        for x in range (0, 8) :
            for y in range (0, 8) :
                tabTmp[x][y] = matrix[i][x][y] / quantizer[i][x][y]
        tab.append(tabTmp)        
    return tab

def deQuantizedMatrix(quantizedMatrix,quantizer) :
    tab = []
    for i in range (0,len(quantizedMatrix)) :
        tabTmp = [[0 for a in range(8)] for b in range(8)]
        for x in range (0, 8) :
            for y in range (0, 8) :
                tabTmp[x][y] = quantizedMatrix[i][x][y] * quantizer[i][x][y]
        tab.append(tabTmp)        
    return tab

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
    for x in range(0,sizeH) :
        for y in range(0,sizeW) :
            img.write(str(MatrixesR[x][y])+"\n")
            img.write(str(MatrixesG[x][y])+"\n")
            img.write(str(MatrixesB[x][y])+"\n")          
    return 

def writeNewImg(img,header,sizeW,sizeH,maxValueOfAByte) :
    img.write(header)
    img.write(str(sizeW)+" "+str(sizeH)+"\n")
    img.write(str(maxValueOfAByte)+"\n")
    for x in range(0,sizeH*sizeW) :
        #R = matrixesYDecompressed[x] + 1.403 * matrixesVDecompressed[x]
        newR = int(1.164*(matrixesYDecompressed[x] - 16) + 1.596 * (matrixesVDecompressed[x] - 128))
        #G = matrixesYDecompressed[x] - 0.344 * matrixesUDecompressed[x] - 0.714 * matrixesVDecompressed[x]
        newG = int(1.164*(matrixesYDecompressed[x] - 16) - 0.813*(matrixesVDecompressed[x] - 128) - 0.391 * (matrixesUDecompressed[x] - 128))
        #B = matrixesYDecompressed[x] + 1.770 * matrixesUDecompressed[x]
        newB = int(1.164*(matrixesYDecompressed[x] - 16) + 2.018 * (matrixesUDecompressed[x] - 128))  
        img.write(str(newR)+"\n")
        img.write(str(newG)+"\n")
        img.write(str(newB)+"\n")           
    return 

#---------- Main ----------
#fileBinary = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/nt-P3.ppm","rb")
fileBinary = open("nt-P3.ppm","rb")

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

print("Ready to get All pixels")
# Fill all matrixes with the pixels
getAllPixel(fileBinary)

print("Ready to Convert matrixes")
# Create Matrixe Y
convertMatrixesToY()
# Create Matrixe U
convertMatrixesToU()
# Create Matrixe V
convertMatrixesToV()

print("Ready to Divided matrixes")
# Get All Matrixes Divided
for i in range(0,sizeH,8) :
    for j in range(0,sizeW,8) :
        matrixesYDivided.append(devideMatrixes(i,j,MatrixesY))
        matrixesUDivided.append(devideMatrixes(i,j,MatrixesU))
        matrixesVDivided.append(devideMatrixes(i,j,MatrixesV))

print("Ready to compress Matrixes U and V")
# Matrixes are Compress ( U - V )
compressMatrixe(matrixesUDivided)
compressMatrixe(matrixesVDivided)

print("Ready to substract 128 to all values")
DiscreteCosineTransform(matrixesYDivided,matrixesUDivided,matrixesVDivided)

print("Ready to create DCT")
matrixesDCTY = ForwardDCT(matrixesYDivided)
matrixesDCTU = ForwardDCT(matrixesUDivided)
matrixesDCTV = ForwardDCT(matrixesVDivided)

print("Ready to Quantized")
quantizer = createQuantizer(2.0)
matrixYQuantized = quantizedMatrix(matrixesDCTY,quantizer)
matrixUQuantized = quantizedMatrix(matrixesDCTU,quantizer)
matrixVQuantized = quantizedMatrix(matrixesDCTV,quantizer)

print("Ready to DeQuantized")
matrixYDeQuantized = deQuantizedMatrix(matrixYQuantized,quantizer)
matrixUDeQuantized = deQuantizedMatrix(matrixUQuantized,quantizer)
matrixVDeQuantized = deQuantizedMatrix(matrixVQuantized,quantizer)

print("Ready to DeQuantized Inverse DCT")
matrixesYInverseDCT = InverseDCT(matrixYDeQuantized)
matrixesUInverseDCT = InverseDCT(matrixUDeQuantized)
matrixesVInverseDCT = InverseDCT(matrixVDeQuantized)

print("Ready to add 128 to all values")
DiscreteCosineTransform(matrixesYInverseDCT,matrixesUInverseDCT,matrixesVInverseDCT)

# test = open('test',"wb")
# test.write(str(quantizer))

print("Ready to Reformat matrixes")
# Reformat Matrixes
matrixesYDecompressed = decompressMatrixes(matrixesYInverseDCT)
matrixesUDecompressed = decompressMatrixes(matrixesUInverseDCT)
matrixesVDecompressed = decompressMatrixes(matrixesVInverseDCT)

print("Ready to Create new Image")
# Create new image
newImage = open("newimage.ppm","wb")
#newImage = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/newimage.ppm","wb")
writeNewImg(newImage,header,sizeW,sizeH,maxValueOfAByte)



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

# filetest = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/testY","wb")
# filetest.write(str(matrixesYDecompressed))

# filetestt = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/testU","wb")
# filetestt.write(str(matrixesUDecompressed))

# filetesttt = open("/Users/cyrilcrozes/Documents/Documents/Document_IMERIR/Roumanie/Audio_Video/testV","wb")
# filetesttt.write(str(matrixesVDecompressed))