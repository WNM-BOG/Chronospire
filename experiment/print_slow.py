import time
import random


def print_slow(text, min_delay=0.02, max_delay=0.05, typing_errors=True):
    punctuation_delays = {
        '.': (0.3, 0.6),
        '!': (0.3, 0.6),
        '?': (0.3, 0.6),
        ',': (0.1, 0.3),
        ';': (0.2, 0.4),
        ':': (0.2, 0.4),
        '\n': (0.1, 0.3)
    }

    i = 0
    while i < len(text):
        char = text[i]

        if typing_errors and char.isalpha() and random.random() < 0.05 and i < len(text) - 1:
            error_chars = {
                'а': 'фы', 'б': 'ьн', 'в': 'фцы', 'г': 'ьр', 'д': 'ыл',
                'е': 'ку', 'ё': 'ку', 'ж': 'эд', 'з': 'ьх', 'и': 'цу',
                'й': 'цы', 'к': 'ен', 'л': 'др', 'м': 'ьт', 'н': 'гк',
                'о': 'лп', 'п': 'ол', 'р': 'кг', 'с': 'вы', 'т': 'ьм',
                'у': 'ге', 'ф': 'яы', 'х': 'чз', 'ц': 'ув', 'ч': 'сх',
                'ш': 'щэ', 'щ': 'шэ', 'ъ': 'эю', 'ы': 'ва', 'ь': 'бю',
                'э': 'ъю', 'ю': 'ъэ', 'я': 'фч'
            }

            if char.lower() in error_chars and error_chars[char.lower()]:
                error_char = random.choice(error_chars[char.lower()])
                print(error_char, end='', flush=True)
                time.sleep(random.uniform(0.05, 0.1))
                print('\b \b', end='', flush=True)
                time.sleep(0.05)

        print(char, end='', flush=True)

        if char in punctuation_delays:
            delay_min, delay_max = punctuation_delays[char]
            delay = random.uniform(delay_min, delay_max)
        elif char == ' ':
            if random.random() < 0.3: 
                delay = random.uniform(0.1, 0.3)
            else:
                delay = random.uniform(min_delay, max_delay)
        else:
            delay = random.uniform(min_delay, max_delay)
            if char.isalpha() and random.random() < 0.1:
                delay *= random.uniform(1.5, 3.0)

        time.sleep(delay)
        i += 1

    print()


print_slow("Судьба вселенной висит на волоске, и только вы можете ее спасти... ")
print_slow("Помните: время не прощает ошибок, и каждая секунда может стать последней.")