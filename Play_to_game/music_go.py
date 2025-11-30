import os
print("=== ПРОВЕРКА ФАЙЛОВ ===")
for file in os.listdir('.'):
    if 'wnm' in file.lower() or 'mp3' in file:
        print(f"Найден файл: {file} (размер: {os.path.getsize(file)} байт)")
        input()
