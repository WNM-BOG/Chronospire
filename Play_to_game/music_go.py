```python
def play_chaos_music():
    try:
        formats = ['WNM.mp3', 'WNM.wav', 'WNM.ogg']

        for format in formats:
            if os.path.exists(format):
                try:
                    pygame.mixer.music.load(format)
                    pygame.mixer.music.play(-1)
                    print(f"Музыка запущена из файла: {format}")
                    return True
                except:
                    print(f"Не удалось воспроизвести {format}, пробуем следующий...")
                    continue

        print("Ни один музыкальный файл не удалось воспроизвести")
        return False

    except Exception as e:
        print(f"Ошибка: {e}")
        return False
```
