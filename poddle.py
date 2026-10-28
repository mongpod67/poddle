import os

appdata = os.environ['LOCALAPPDATA']

tabstate = os.path.join(appdata, 'Packages',
                        'Microsoft.WindowsNotepad_8wekyb3d8bbwe', 
                        'LocalState', 'TabState') # notepad tab state folder

def hex_dump(data: bytes, width: int = 16) -> str:
    lines = []

    for offset in range(0, len(data), width):
        chunk = data[offset:offset + width]

        hex_part = " ".join(f"{b:02X}" for b in chunk)
        ascii_part = "".join(
            chr(b) if 32 <= b < 127 else "."
            for b in chunk
        )

        lines.append(
            f"{offset:08X}  "
            f"{hex_part:<{width * 3 - 1}}  "
            f"|{ascii_part}|"
        )

    return "\n".join(lines)

for file in os.listdir(tabstate):
    if file[-6:] in ('.0.bin', '.1.bin'): # these files do not contain useful data
        continue

    print('----------------------------------------')

    with open(os.path.join(tabstate, file), 'rb') as f:
        data = f.read()

    cleaned = data[:-4] # remove checksum

    dlen = ((cleaned[0x10] & 0x7f) + (cleaned[0x11] << 7)) * 2 # calculate data length

    body = cleaned[0x12:0x12+dlen] # extract data

    print(f'File: {file}')
    print(f'Length: {len(body)//2}')
    text = body.decode('utf-16-le')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = text.replace('\n', '\r\n')

    print(f'Body:\n{text}')
    print(f'Data (hex):\n{hex_dump(data)}')
    print('----------------------------------------')