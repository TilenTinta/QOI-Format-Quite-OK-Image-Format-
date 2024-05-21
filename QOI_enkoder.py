###########################################################
######## Title: IIK - projekt 7                    ########
######## Author: Tilen Tinta                       ########
######## Program: BMS 1, Avtomatika in Informatika ########
######## Date: May, 2024                           ########
###########################################################

from PIL import Image


def qoiHeader(width, height, mode): # 14 bajtov
    # Magic - prvi 4 bajti
    magic = b'qoif' 

    # Width, Height - vsak po 4 bajte (8 bytov)

    # Channels, Colorspace - vsak po 1 byte (2 bajta)
    if mode == 'RGB':
        channels = 3
        colorspace = 1
    if mode == 'RGBA':
        channels = 4
        colorspace = 1 # ali 0? vseeno za file ampak javi drugačnost

    header = magic + int(width).to_bytes(4,'big') + int(height).to_bytes(4,'big') + channels.to_bytes(1,'big') + colorspace.to_bytes(1,'big')
    return header


def qoiHash(pixel):
    # Hash je ostanek
    return (pixel[0] * 3 + pixel[1] * 5 + pixel[2] * 7 + pixel[3] * 11) % 64

if __name__ == "__main__":

    # Uvozi datoteko
    image = Image.open('./Slike/qoi_test_images/monument.png') # kodim23

    # Podatki iz datoteke
    #print(image.format)
    width, height = image.size
    mode = image.mode
    #print(mode)
    piksli = list(image.getdata()) # (r, g, b, "a")

    # Header, end #
    qoi_header = qoiHeader(width, height, mode)
    qoi_end_marker = b'\x00\x00\x00\x00\x00\x00\x00\x01'
    #print(header)    


    array = [[0, 0, 0, 0]] * 64 
    pxOld = [0, 0, 0, 255]
    zaporedje = 0
    pixelEncoded = bytearray()
    velikost = len(piksli)

    # Oznake operacij
    QOI_OP_RUN   = 0b11000000
    QOI_OP_INDEX = 0b00000000
    QOI_OP_DIFF  = 0b01000000
    QOI_OP_LUMA  = 0b10000000 #0x80
    QOI_OP_RGB   = 0b11111110
    QOI_OP_RGBA  = 0b11111111

    # Kodiranje
    for i in range(0, velikost):

        px = list(piksli[i]) # Trenuten pixel
        if mode == 'RGB':
            px.append(255)

        if px == pxOld:
            zaporedje += 1
            # QOI_OP_RUN # 
            if zaporedje == 62 or i == (velikost - 1): # če ni (velikost - 1) zadnje iteracije ne shrani
                pixelEncoded.append(QOI_OP_RUN | (zaporedje - 1)) # -1 zaradi primera samo enega pixla
                zaporedje = 0
        else:
            # QOI_OP_RUN #
            if zaporedje > 0:
                pixelEncoded.append(QOI_OP_RUN | (zaporedje - 1)) # -1 zaradi primera samo enega pixla
                zaporedje = 0

            Index = qoiHash(px) # Računanje indeksa

            # QOI_OP_INDEX #
            if array[Index] == px:
                pixelEncoded.append(QOI_OP_INDEX | Index)
            else:
                array[Index] = px  

                if (len(px) == 4 and (px[3] - pxOld[3]) == 0) or len(px) == 3:  
                    # Računanje delte barve
                    dr = px[0] - pxOld[0]
                    dg = px[1] - pxOld[1]
                    db = px[2] - pxOld[2]
                    dr_dg = dr - dg
                    db_dg = db - dg
                    
            # QOI_OP_DIFF #
                    if (dr <= 1 and dr >= -2) and (dg <= 1 and dg >= -2) and (db <= 1 and db >= -2):
                        dr += 2
                        dg += 2
                        db += 2
                        colorBiti = QOI_OP_DIFF | (dr << 4) | (dg << 2) | db
                        pixelEncoded.append(colorBiti)
                        
            # QOI_OP_LUMA #    
                    elif (dg >= -32 and dg <= 31) and (dr_dg >= -8 and dr_dg <= 7) and (db_dg >= -8 and db_dg <= 7):
                        dg += 32
                        dr_dg += 8
                        db_dg += 8 
                        pixelEncoded.append(QOI_OP_LUMA | dg) 
                        pixelEncoded.append((dr_dg << 4) | db_dg)
                    else:
            # QOI_OP_RGB #
                        pixelEncoded.append(QOI_OP_RGB)
                        pixelEncoded.append(px[0])
                        pixelEncoded.append(px[1])
                        pixelEncoded.append(px[2])
                else:
            # QOI_OP_RGBA #
                    pixelEncoded.append(QOI_OP_RGBA)
                    pixelEncoded.extend(px)
                    #pixelEncoded.append(px[1])
                    #pixelEncoded.append(px[2])
                    #pixelEncoded.append(px[3])

        pxOld = px

    # Končni file
    qoiOutput = qoi_header + pixelEncoded + qoi_end_marker
        
    # Shrani file
    with open('output.qoi', 'wb') as file:
        file.write(qoiOutput)
    