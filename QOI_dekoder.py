###########################################################
######## Title: IIK - projekt 7                    ########
######## Author: Tilen Tinta                       ########
######## Program: BMS 1, Avtomatika in Informatika ########
######## Date: May, 2024                           ########
###########################################################

from PIL import Image


if __name__ == "__main__":

    # Uvozi datoteko
    with open('output.qoi', 'rb') as file:
        qoiFile = file.read()

    # Header, end #
    qoi_end_marker = b'\x00\x00\x00\x00\x00\x00\x00\x01'   

    array = [(0, 0, 0, 0)] * 64 
    pxOld = (0, 0, 0, 255)
    zaporedje = 0
    pixelEncoded = bytearray()
    #velikost = (width * height)

    header = qoiFile[:14]
    name = header[:4]
    width = header[4:8]
    height = header[8:12]
    channels = header[12]
    colorspace = header[13]
    print(int.from_bytes(width))
    print(int.from_bytes(height))
    #for i in range(velikost):
    #    if i < 14:
        

       

    # Končni file
    #qoiOutput = qoi_header + pixelEncoded + qoi_end_marker
        
    # Shrani file
    