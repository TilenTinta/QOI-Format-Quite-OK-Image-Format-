###########################################################
######## Title: IIK - projekt 7                    ########
######## Author: Tilen Tinta                       ########
######## Program: BMS 1, Avtomatika in Informatika ########
######## Date: May, 2024                           ########
###########################################################

from PIL import Image
import numpy as np


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


def QOI_encoder(image):

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

    return qoiOutput
        
    


def QOI_decoder(qoiFile):

    # Oznake operacij
    QOI_OP_RUN   = 0b11000000
    QOI_OP_INDEX = 0b00000000
    QOI_OP_DIFF  = 0b01000000
    QOI_OP_LUMA  = 0b10000000
    QOI_OP_RGB   = 0b11111110
    QOI_OP_RGBA  = 0b11111111

    QOI_op_maska = 0b11000000 # maska za ukaz
    QOI_op_data  = 0b00111111 # maska za podatke
    QOI_df_red   = 0b00110000 # maska za razliko rdeče
    QOI_df_green = 0b00001100 # maska za razliko zelene
    QOI_df_blue  = 0b00000011 # maska za razliko modre
    QOI_luma_dg  = 0b00111111 # maska za luma zeleno
    QOI_luma_rg  = 0b11110000 # maska za luma rdečo
    QOI_luma_bg  = 0b00001111 # maska za luma modro


    # Header, end #
    header = qoiFile[:14]
    name = header[:4]
    if name != b"qoif":
        print("Datoteka ni qoi formata!")
        exit(0)
    width = int.from_bytes(header[4:8])
    height = int.from_bytes(header[8:12])
    channels = int(header[12])
    colorspace = int(header[13])

    qoi_end_marker = b'\x00\x00\x00\x00\x00\x00\x00\x01'   

    buffer = qoiFile[14:(len(qoiFile) - len(qoi_end_marker))] # buffer pixlov brez headerja in konca

    array = [[0, 0, 0, 0]] * 64 
    px = [0, 0, 0, 255]
    bufferEnd = bytearray()

    # Dekodiranje
    i = 0
    while i < len(buffer):

        byte = buffer[i]
            
        # QOI_OP_RGB #
        if byte == QOI_OP_RGB:
            px[0] = buffer[i + 1]
            px[1] = buffer[i + 2]
            px[2] = buffer[i + 3]
            bufferEnd.extend(px[:channels])
            i += 4
        
        # QOI_OP_RGBA #
        elif byte == QOI_OP_RGBA:
            px[0] = buffer[i + 1]
            px[1] = buffer[i + 2]
            px[2] = buffer[i + 3]
            px[3] = buffer[i + 4]
            bufferEnd.extend(px[:channels])
            i += 5

        # QOI_OP_INDEX #
        elif (QOI_op_maska & byte) == QOI_OP_INDEX:
            index = (byte & QOI_op_data)
            px = array[index]
            bufferEnd.extend(px[:channels])
            i += 1

        # QOI_OP_DIFF #
        elif (QOI_op_maska & byte) == QOI_OP_DIFF:
            data = (byte & QOI_op_data)
            dr = ((data & QOI_df_red) >> 4) - 2
            dg = ((data & QOI_df_green) >> 2) - 2
            db = (data & QOI_df_blue) - 2
            px[0] = (px[0] + dr) & 0xFF
            px[1] = (px[1] + dg) & 0xFF
            px[2] = (px[2] + db) & 0xFF
            bufferEnd.extend(px[:channels])
            i += 1

        # QOI_OP_LUMA #
        elif (QOI_op_maska & byte) == QOI_OP_LUMA:
            byte2 = buffer[i + 1]
            dg = (byte & QOI_luma_dg) - 32 # bias
            drdg = ((byte2 & QOI_luma_rg) >> 4) - 8
            dbdg = (byte2 & QOI_luma_bg) - 8

            dr = drdg + dg
            db = dbdg + dg

            px[0] = (px[0] + dr) & 0xFF
            px[1] = (px[1] + dg) & 0xFF
            px[2] = (px[2] + db) & 0xFF
            bufferEnd.extend(px[:channels])
            i += 2

        # QOI_OP_RUN #
        elif (QOI_op_maska & byte) == QOI_OP_RUN:
            run = (byte & QOI_op_data) + 1 # bias
            for j in range(run):
                bufferEnd.extend(px[:channels])
            i += 1
            
        array[qoiHash(px)] = px[:]
        

    # Shrani file
    if channels == 4:
        pic = np.array(bufferEnd, dtype=np.uint8).reshape((height, width, 4))
        image = Image.fromarray(pic, 'RGBA')
    else:
        pic = np.array(bufferEnd, dtype=np.uint8).reshape((height, width, 3))
        image = Image.fromarray(pic, 'RGB')

    return image

    
    