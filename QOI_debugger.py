# Python script to inspect a QOI file

def inspect_qoi_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        
    # Check header
    magic = data[:4]
    width = int.from_bytes(data[4:8], 'big')
    height = int.from_bytes(data[8:12], 'big')
    channels = data[12]
    colorspace = data[13]
    
    print(f"Magic: {magic}")
    print(f"Width: {width}")
    print(f"Height: {height}")
    print(f"Channels: {channels}")
    print(f"Colorspace: {colorspace}")
    
    # Check data chunks
    i = 14
    while i < len(data) - 8:
        byte = data[i]
        if byte == 0b11111110:  # QOI_OP_RGB
            print(f"QOI_OP_RGB at byte {i}")
            i += 4
        elif byte == 0b11111111:  # QOI_OP_RGBA
            print(f"QOI_OP_RGBA at byte {i}")
            i += 5
        elif (byte & 0b11000000) == 0b00000000:  # QOI_OP_INDEX
            index = byte & 0b00111111
            print(f"QOI_OP_INDEX at byte {i}, index {index}")
            i += 1
        elif (byte & 0b11000000) == 0b01000000:  # QOI_OP_DIFF
            print(f"QOI_OP_DIFF at byte {i}")
            i += 1
        elif (byte & 0b11000000) == 0b10000000:  # QOI_OP_LUMA
            print(f"QOI_OP_LUMA at byte {i}")
            i += 2
        elif (byte & 0b11000000) == 0b11000000:  # QOI_OP_RUN
            print(f"QOI_OP_RUN at byte {i}")
            i += 1
        else:
            print(f"Unknown byte {byte} at position {i}")
            break
    
    # Check end marker
    end_marker = data[-8:]
    print(f"End Marker: {end_marker}")
    
    if end_marker == b'\x00\x00\x00\x00\x00\x00\x00\x01':
        print("End marker is correct.")
    else:
        print("End marker is incorrect.")

# Run the function with the path to your QOI file
inspect_qoi_file('output.qoi')
