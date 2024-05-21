###########################################################
######## Title: IIK - projekt 7                    ########
######## Author: Tilen Tinta                       ########
######## Program: BMS 1, Avtomatika in Informatika ########
######## Date: May, 2024                           ########
###########################################################

from PIL import Image
import QOI as qoi


if __name__ == "__main__":

    # Nastavi vhodno datoteko in izhodni format datoteke
    inputFile = './Slike/qoi_test_images/monument.png'
    outputFormat = '.png'

    ### Kodiranje datoteke ###

    # Uvozi datoteko
    image = Image.open(inputFile) # kodim23

    qoiOutput = qoi.QOI_encoder(image)

    # Shrani file
    with open('output.qoi', 'wb') as file:
        file.write(qoiOutput)

    ### Dekodiranje datoteke ###

    # Uvozi datoteko
    file = 'output.qoi'
    with open(file, 'rb') as file:
        qoiFile = file.read()

    # Shrani
    image = qoi.QOI_decoder(qoiFile)
    image.show() # pokaži sliko
    image.save('output' + outputFormat)