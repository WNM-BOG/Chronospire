import os
for file in os.listdir('.'):
    if 'wnm' in file.lower():
        os.rename(file, 'WNM.mp3')
        print(f"Файл переименован в WNM.mp3")
        input()
        break
