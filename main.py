###########################################################
######## Title: IIK - projekt 7                    ########
######## Author: Tilen Tinta                       ########
######## Program: BMS 1, Avtomatika in Informatika ########
######## Date: May, 2024                           ########
###########################################################

from PIL import Image
import QOI as qoi
import numpy as np
import os
import matplotlib.pyplot as plt
import time


if __name__ == "__main__":

    #######################
    #### Naloga 1 in 2 ####
    #######################

    ### Nastavi vhodno datoteko in izhodni format datoteke ###
    inputFile = './Slike/qoi_test_images/kodim23.png'
    outputFormat = '.png' # .jpg, .bmp...


    ### Kodiranje datoteke ###
    # Uvozi datoteko
    image = Image.open(inputFile)
    qoiOutput = qoi.QOI_encoder(image)

    # Shrani file
    with open('output.qoi', 'wb') as file:
        file.write(qoiOutput)


    ### Dekodiranje datoteke ###
    # Uvozi datoteko
    file = 'output.qoi'
    with open(file, 'rb') as file:
        qoiFile = file.read()
    
    image = qoi.QOI_decoder(qoiFile, 0)
    # Shrani
    image.show() # pokaži sliko
    image.save('output' + outputFormat)



    ######################
    ###### Naloga 3 ######
    ######################
    timeEncode = []
    timeDecode= []

    ### Nastavi vhodno datoteko in izhodni format datoteke ###
    # 3.1 - Kodiranje in dekodiranje vseh slik v različne formate (preverjanje napak: OK!)
    for i in range(24):
        num = i + 1
        if num < 10: 
            num = '0' + str(num)
        else:
            num = str(num)
        inputFile = './Slike/archive/kodim' + str(num) + '.png'


        ### Kodiranje datoteke ###
        timeStart = time.time()
        # Uvozi datoteko
        image = Image.open(inputFile)
        qoiOutput = qoi.QOI_encoder(image)

        # Shrani file
        with open('./Slike/archive/QOI/kodim' + num + '.qoi', 'wb') as file:
            file.write(qoiOutput)

        timeEnd = time.time()
        timeEncode.append((timeEnd-timeStart))


        ### Dekodiranje datoteke ###
        # Uvozi datoteko
        timeStart = time.time()
        file = './Slike/archive/QOI/kodim' + num + '.qoi'
        with open(file, 'rb') as file:
            qoiFile = file.read()

        # Shrani
        image = qoi.QOI_decoder(qoiFile, 0)
        image.save('./Slike/archive/NewPNG/kodim' + num + '.png')
        timeEnd = time.time()
        timeDecode.append((timeEnd-timeStart))
        image.save('./Slike/archive/NewBMP/kodim' + num + '.bmp')

    avgTimeEncode = sum(timeEncode) / len(timeEncode)
    avgTimeDecode = sum(timeDecode) / len(timeDecode)
    print("Povprečen čas kodiranja:", avgTimeEncode)
    print("Povprečen čas dekodiranja:", avgTimeDecode)


    # 3.2 - Srednja kvadratna napaka
    for i in range(24):
        num = i + 1
        if num < 10: 
            num = '0' + str(num)
        else:
            num = str(num)
        inputFilePNG = './Slike/archive/kodim' + str(num) + '.png' 
        inputFileQOI = './Slike/archive/QOI/kodim' + str(num) + '.qoi'

        # Uvozi png datoteko
        image = Image.open(inputFilePNG)
        piksliPNG = list(image.getdata()) 

        # Uvozi datoteko
        file = inputFileQOI
        with open(file, 'rb') as file:
            qoiFile = file.read()

        piksliQOI = qoi.QOI_decoder(qoiFile, 1)


        arr1 = np.array(piksliPNG)
        arr2 = np.array(piksliQOI)
        
        # Izračunajte srednjo kvadratno napako
        mse_value = np.mean((arr1 - arr2) ** 2)
        print("MSE med datotekama kodim" + str(num) + ".jpg in .qoi:", mse_value)
        
        
    # 3.3 - povprečna velikost
    velikostiPNG = []
    velikostiBMP = []
    velikostiQOI = []

    for i in range(24):
        num = i + 1
        if num < 10: 
            num = '0' + str(num)
        else:
            num = str(num)
        inputFileBMP = './Slike/archive/NewBMP/kodim' + str(num) + '.bmp' 
        inputFilePNG = './Slike/archive/kodim' + str(num) + '.png' 
        inputFileQOI = './Slike/archive/QOI/kodim' + str(num) + '.qoi'

        velikostiBMP.append(os.path.getsize(inputFileBMP))
        velikostiPNG.append(os.path.getsize(inputFilePNG))
        velikostiQOI.append(os.path.getsize(inputFileQOI))

    avgSizeBMP = sum(velikostiBMP) / len(velikostiBMP)
    avgSizePNG = sum(velikostiPNG) / len(velikostiPNG)
    avgSizeQOI = sum(velikostiQOI) / len(velikostiQOI)

    formats = ['BMP', 'PNG', 'QOI']
    avgSizes = [avgSizeBMP, avgSizePNG, avgSizeQOI]
    
    plt.bar(formats, avgSizes, color=['blue', 'green', 'red'])
    plt.xlabel('Format')
    plt.ylabel('Povprečna velikost datoteke (bajti)')
    plt.title('Povprečna velikost datotek po formatih')
    plt.show()