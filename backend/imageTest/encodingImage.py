import base64


with open("a.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print(encoded_string)
    with open("img64.txt", 'w') as txtFile:
        txtFile.write(str(encoded_string))
        
