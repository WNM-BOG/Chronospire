import random
import time
import sys
import os

player_name = ""
player_class = ""
player_level = 1
player_exp = 0
exp_to_next_level = 100
player_health = 100
player_max_health = 100
player_attack = 10
player_defense = 10
player_dodge = 5
player_stat_points = 0
player_inventory = []
current_location = 0
game_running = True
player_alive = True
location_visited = [False] * 8
game_difficulty = "средняя"
final_boss_defeated = False
hidden_boss_defeated = False
equipped_weapon = None
equipped_armor = None
player_gold = 100

difficulty_multipliers = {
    "лёгкая": {"player_health": 1.5, "player_attack": 1.3, "player_defense": 1.3,
               "enemy_health": 0.6, "enemy_attack": 0.6, "enemy_defense": 0.6, "exp_gain": 1.5},
    "средняя": {"player_health": 1.2, "player_attack": 1.1, "player_defense": 1.1,
                "enemy_health": 0.8, "enemy_attack": 0.8, "enemy_defense": 0.8, "exp_gain": 1.2},
    "сложная": {"player_health": 1.0, "player_attack": 1.0, "player_defense": 1.0,
                "enemy_health": 1.0, "enemy_attack": 1.0, "enemy_defense": 1.0, "exp_gain": 1.0},
    "безумная": {"player_health": 0.8, "player_attack": 0.9, "player_defense": 0.9,
                 "enemy_health": 1.5, "enemy_attack": 1.5, "enemy_defense": 1.5, "exp_gain": 1.2},
    "невозможная": {"player_health": 0.6, "player_attack": 0.8, "player_defense": 0.8,
                    "enemy_health": 2.0, "enemy_attack": 2.0, "enemy_defense": 2.0, "exp_gain": 1.5}
}

locations = [
    {
        "name": "Врата Хроноспирали",
        "description": "Вы стоите перед древними вратами, ведущими к богам времени. Воздух дрожит от энергии веков. Каменные плиты под ногами исписаны рунами, которые меняются прямо на глазах. Врата пульсируют таинственным светом, призывая вас войти.",
        "type": "бой"
    },
    {
        "name": "Зал Прошлого",
        "description": "Фрески на стенах изображают былые времена. Здесь время течет иначе. Вы видите события, которые уже произошли, и те, что еще только случатся. Эхо ваших шагов звучит так, будто вы идете по коридору воспоминаний.",
        "type": "сундук"
    },
    {
        "name": "Мост Судьбы",
        "description": "Радужный мост простирается через бездну. Каждый шаг отзывается эхом в вечности. Под вами простирается бесконечная пустота, усеянная звездами и осколками времени. Воздух наполнен энергией, которая заставляет кожу покалывать.",
        "type": "бой"
    },
    {
        "name": "Сад Вечности",
        "description": "Место покоя и восстановления. Древние деревья шепчут тайны вселенной. Цветы здесь никогда не увядают, а фонтаны изливают воду, которая искрится всеми цветами радуги. Это оазис спокойствия перед грядущими битвами.",
        "type": "отдых"
    },
    {
        "name": "Чертоги Богов",
        "description": "Здесь обитают повелители времени. Воздух наполнен их могуществом. Стены из чистого света образуют залы невообразимых размеров. Вы чувствуете, как взгляды невидимых существ следят за вашим каждым движением.",
        "type": "бой"
    },
    {
        "name": "Сокровищница Времени",
        "description": "Легендарные артефакты хранятся здесь. Сокровища, способные изменить реальность. Сундуки из чистого времени содержат оружие и доспехи, созданные в эпоху рождения вселенной. Каждый предмет здесь имеет свою историю и силу.",
        "type": "сундук"
    },
    {
        "name": "Престол Хроноса",
        "description": "Финальное испытание. Здесь вы встретитесь с верховным богом времени. Престол высечен из кристалла времени и парит в центре зала, окруженный вихрями временных потоков. Это место, где решается судьба вселенной.",
        "type": "финальный бой"
    },
    {
        "name": "Измерение Забвения",
        "description": "Скрытое измерение, доступное лишь тем, кто прошел невозможные испытания. Здесь обитает Первозданный Хаос - существо, существовавшее до рождения времени. Воздух наполнен первозданной энергией, а реальность искажается с каждым мгновением.",
        "type": "скрытый бой",
        "required_difficulty": "невозможная"
    }
]

items = {
    "зелье_здоровья": {"name": "Зелье здоровья", "type": "зелье", "effect": "heal", "value": 50,
                       "description": "Восстанавливает 50 единиц здоровья", "price": 50},
    "зелье_силы": {"name": "Зелье силы", "type": "зелье", "effect": "attack", "value": 10,
                   "description": "Увеличивает атаку на 10 до конца боя", "price": 75},
    "меч_воина": {"name": "Меч воина", "type": "оружие", "effect": "attack", "value": 15,
                  "description": "Острое клинковое оружие, увеличивает атаку на 15", "price": 200},
    "посох_мага": {"name": "Посох мага", "type": "оружие", "effect": "attack", "value": 20,
                   "description": "Древний посох, усиливающий магические способности, увеличивает атаку на 20",
                   "price": 300},
    "щит_защиты": {"name": "Щит защиты", "type": "броня", "effect": "defense", "value": 15,
                   "description": "Прочный щит, увеличивает защиту на 15", "price": 250},
    "эликсир_богов": {"name": "Эликсир богов", "type": "зелье", "effect": "heal", "value": 200,
                      "description": "Легендарный эликсир, восстанавливающий 200 единиц здоровья", "price": 200},
    "плащ_теней": {"name": "Плащ теней", "type": "броня", "effect": "dodge", "value": 10,
                   "description": "Плащ, сотканный из теней, увеличивает уклонение на 10%", "price": 250},
    "кольцо_могущества": {"name": "Кольцо могущества", "type": "оружие", "effect": "attack", "value": 25,
                          "description": "Древнее кольцо, наделяющее владельца невероятной силой", "price": 400},
    "артефакт_хаоса": {"name": "Артефакт Хаоса", "type": "оружие", "effect": "attack", "value": 40,
                       "description": "Древний артефакт, содержащий силу Первозданного Хаоса", "price": 600}
}

base_enemies = [
    {"name": "Страж Бездны", "health": 50, "attack": 15, "defense": 10, "exp": 50, "gold": 25,
     "description": "Могучий страж, охраняющий врата Хроноспирали. Его доспехи сделаны из застывшего времени."},
    {"name": "Небесный Каратель", "health": 40, "attack": 20, "defense": 5, "exp": 60, "gold": 30,
     "description": "Крылатый воин, несущий гнев богов. Его клинок пронзает саму реальности."},
    {"name": "Хранитель Времени", "health": 60, "attack": 12, "defense": 15, "exp": 70, "gold": 35,
     "description": "Древнее существо, контролирующее потоки времени. Может предвидеть ваши атаки."},
    {"name": "Бог Хронос", "health": 200, "attack": 30, "defense": 20, "exp": 0, "gold": 500,
     "description": "Верховный бог времени. Его могущество не знает границ. Он контролирует само течение времени."},
    {"name": "Первозданный Хаос", "health": 400, "attack": 50, "defense": 30, "exp": 0, "gold": 666,
     "description": "Существо, существовавшее до рождения времени. Его сила не поддается пониманию смертных."}
]


def get_enemy(enemy_index):
    base_enemy = base_enemies[enemy_index].copy()
    multiplier = difficulty_multipliers[game_difficulty]

    if enemy_index == 3 and game_difficulty == "невозможная":
        base_enemy["exp"] = 500
    elif enemy_index == 4:
        base_enemy["exp"] = 2000
        base_enemy["gold"] = 1000

    enemy = {
        "name": base_enemy["name"],
        "health": int(base_enemy["health"] * multiplier["enemy_health"]),
        "max_health": int(base_enemy["health"] * multiplier["enemy_health"]),
        "attack": int(base_enemy["attack"] * multiplier["enemy_attack"]),
        "defense": int(base_enemy["defense"] * multiplier["enemy_defense"]),
        "exp": int(base_enemy["exp"] * multiplier["exp_gain"]),
        "gold": base_enemy["gold"],
        "description": base_enemy["description"]
    }

    return enemy

def show_title():
    print("=" * 80)
    print(" " * 32 + "ХРОНОСПИРАЛЬ")
    print("=" * 80)
    print(" " * 21 + "Эпическая сага о мести богам времени")
    print("=" * 80)
    print()


def print_slow(text, min_delay=0.02, max_delay=0.05):
    for chr in text:
        print(chr, end='', flush=True)
        time.sleep(random.uniform(min_delay, max_delay))
    print()


def show_intro():
    print_slow("Давным-давно, в эпоху рождения вселенной, боги времени установили свое владычество.")
    print_slow("Они играли судьбами смертных, как пешками в своей вечной игре.")
    print_slow("Города возводились и рушились по их воле, цивилизации рождались и умирали в мгновение ока.")
    print_slow("Но однажды они совершили роковую ошибку - уничтожили всё, что ты любил.")
    print_slow("Твою семью, твой народ, твой мир - всё стерли с лица реальности.")
    print_slow("\nТеперь ты поднимаешься по Хроноспирали - лестнице, соединяющей миры и времена.")
    print_slow("Твоя цель - достичь Престола Хроноса и свергнуть повелителей времени.")
    print_slow("Ты будешь сражаться с стражами богов, преодолевать ловушки времени и бросать вызов самим божествам.")
    print_slow("\nСудьба вселенной висит на волоске, и только ты можешь ее спасти...")
    print_slow("Но помни: время не прощает ошибок, и каждая секунда может стать последней.")
    print()


def choose_difficulty():
    global game_difficulty
    time.sleep(0.2)
    print()
    print("=" * 60)
    time.sleep(0.2)
    print("\t" * 3 + "ВЫБОР СЛОЖНОСТИ")
    time.sleep(0.2)
    print("=" * 60)
    time.sleep(0.2)
    print("Выберите уровень сложности игры:")
    time.sleep(0.2)
    print("\t1: Лёгкая - для начинающих искателей приключений")
    time.sleep(0.2)
    print("\t2: Средняя - сбалансированный игровой опыт")
    time.sleep(0.2)
    print("\t3: Сложная - испытание для опытных воинов")
    time.sleep(0.2)
    print("\t4: Безумная - выживание на грани возможного")
    time.sleep(0.2)
    print("\t5: Невозможная - вызов для истинных мастеров")
    time.sleep(0.2)

    while True:
        choice = input("\nВаш выбор (1-5): ")

        if choice == "1":
            game_difficulty = "лёгкая"
            break
        elif choice == "2":
            game_difficulty = "средняя"
            break
        elif choice == "3":
            game_difficulty = "сложная"
            break
        elif choice == "4":
            game_difficulty = "безумная"
            break
        elif choice == "5":
            game_difficulty = "невозможная"
            break
        else:
            print("Неверный выбор! Пожалуйста, введите число от 1 до 5.")

    print(f"\nВыбрана сложность: {game_difficulty.upper()}")
    show_difficulty_info()


def show_difficulty_info():
    multiplier = difficulty_multipliers[game_difficulty]

    print("\nНастройки сложности:")
    print(f"\tЗдоровье игрока: {multiplier['player_health']}x")
    print(f"\tАтака игрока: {multiplier['player_attack']}x")
    print(f"\tЗащита игрока: {multiplier['player_defense']}x")
    print(f"\tЗдоровье врагов: {multiplier['enemy_health']}x")
    print(f"\tАтака врагов: {multiplier['enemy_attack']}x")
    print(f"\tЗащита врагов: {multiplier['enemy_defense']}x")
    print(f"\tПолучаемый опыт: {multiplier['exp_gain']}x")

    if game_difficulty == "лёгкая":
        print("\nРекомендуется для новичков. Враги слабее, вы получаете больше опыта.")
    elif game_difficulty == "средняя":
        print("\nСбалансированная сложность. Подходит для большинства игроков.")
    elif game_difficulty == "сложная":
        print("\nИстинный вызов. Враги сильны, требуется тактика и планирование.")
    elif game_difficulty == "безумная":
        print("\nЭкстрим! Каждая битва может стать последней. Только для опытных.")
    elif game_difficulty == "невозможная":
        print("\nЛегендарная сложность. Шансы против вас, но слава будет вечной!")
        print("\t★ Доступ к скрытому боссу: ДА ★")

    input("\nНажмите Enter чтобы продолжить...")


def get_total_attack():
    total = player_attack
    if equipped_weapon:
        total += equipped_weapon["value"]
    return total


def get_total_defense():
    total = player_defense
    if equipped_armor and equipped_armor["effect"] == "defense":
        total += equipped_armor["value"]
    return total


def get_total_dodge():
    total = player_dodge
    if equipped_armor and equipped_armor["effect"] == "dodge":
        total += equipped_armor["value"]
    return total


def show_player_stats():
    print("\n" + "=" * 60)
    print(f"\tХАРАКТЕРИСТИКИ {player_name.upper()}")
    print("=" * 60)
    print(f"\tКласс: {player_class}")
    print(f"\tУровень: {player_level}")
    print(f"\tОпыт: {player_exp}/{exp_to_next_level}")
    print(f"\tЗдоровье: {player_health}/{player_max_health}")
    print(f"\tАтака: {get_total_attack()} (база: {player_attack})")
    print(f"\tЗащита: {get_total_defense()} (база: {player_defense})")
    print(f"\tУклонение: {get_total_dodge()}% (база: {player_dodge}%)")
    print(f"\tЗолото: {player_gold} 💰")
    print(f"\tСвободные очки характеристик: {player_stat_points}")
    print(f"\n\tЭкипировка:")
    print(f"\t\tОружие: {equipped_weapon['name'] if equipped_weapon else 'нет'}")
    print(f"\t\tБроня: {equipped_armor['name'] if equipped_armor else 'нет'}")

    if player_inventory:
        print("\n\tИнвентарь:")
        for i, item in enumerate(player_inventory, 1):
            print(f"\t\t{i}: {item['name']} - {item['description']}")
    else:
        print("\n\tИнвентарь: пуст")

    print("=" * 60)


def create_character():
    global player_name, player_class, player_health, player_max_health, player_attack, player_defense, player_dodge
    global equipped_weapon, equipped_armor

    print()
    print("=" * 60)
    print("\t" * 2 + "СОЗДАНИЕ ПЕРСОНАЖА")
    print("=" * 60)

    while True:
        player_name = input("Введите имя вашего героя: ")
        if player_name.strip() != "":
            break
        else:
            print("Имя не может быть пустым! Пожалуйста, введите имя вашего героя.")

    print("\nВыберите класс героя:")
    print("\t1: Воин - сильный и выносливый боец ближнего боя")
    print("\t\tПреимущества: высокое здоровье, хорошая атака и защита")
    print("\t\tНачальные предметы: Меч воина")
    print("\n\t2: Маг - могущественный заклинатель, владеющий магией времени")
    print("\t\tПреимущества: высокая атака, способность ослаблять врагов")
    print("\t\tНачальные предметы: Посох мага")
    print("\n\t3: Ассасин - ловкий и хитрый воин, мастер уклонений")
    print("\t\tПреимущества: высокое уклонение, критический урон")
    print("\t\tНачальные предметы: Плащ теней")

    class_choice = input("\nВаш выбор (1-3): ")

    multiplier = difficulty_multipliers[game_difficulty]

    if class_choice == "1":
        player_class = "Воин"
        base_health = 150
        base_attack = 15
        base_defense = 15
        base_dodge = 5
        if player_name.lower() == "иван" or player_name.lower() == "ваня":
            base_health += 25
            base_attack += 25
            base_defense += 25
            base_dodge += 25
        else:
            pass

        player_health = int(base_health * multiplier["player_health"])
        player_max_health = player_health
        player_attack = int(base_attack * multiplier["player_attack"])
        player_defense = int(base_defense * multiplier["player_defense"])
        player_dodge = base_dodge
        equipped_weapon = items["меч_воина"]
        player_inventory.append(items["зелье_здоровья"])

    elif class_choice == "2":
        player_class = "Маг"
        base_health = 80
        base_attack = 25
        base_defense = 5
        base_dodge = 5
        if player_name.lower() == "иван" or player_name.lower() == "ваня":
            base_health += 25
            base_attack += 25
            base_defense += 25
            base_dodge += 25
        else:
            pass

        player_health = int(base_health * multiplier["player_health"])
        player_max_health = player_health
        player_attack = int(base_attack * multiplier["player_attack"])
        player_defense = int(base_defense * multiplier["player_defense"])
        player_dodge = base_dodge
        equipped_weapon = items["посох_мага"]
        player_inventory.append(items["зелье_здоровья"])
        player_inventory.append(items["зелье_силы"])

    elif class_choice == "3":
        player_class = "Ассасин"
        base_health = 75
        base_attack = 25
        base_defense = 5
        base_dodge = 25
        if player_name.lower() == "иван" or player_name.lower() == "ваня":
            base_health += 25
            base_attack += 25
            base_defense += 25
            base_dodge += 25
        else:
            pass
        player_health = int(base_health * multiplier["player_health"])
        player_max_health = player_health
        player_attack = int(base_attack * multiplier["player_attack"])
        player_defense = int(base_defense * multiplier["player_defense"])
        player_dodge = base_dodge
        equipped_armor = items["плащ_теней"]
        player_inventory.append(items["зелье_здоровья"])

    else:
        print("Неверный выбор! Вы автоматически становитесь Воином.")
        player_class = "Воин"
        base_health = 150
        base_attack = 15
        base_defense = 15
        base_dodge = 5

        player_health = int(base_health * multiplier["player_health"])
        player_max_health = player_health
        player_attack = int(base_attack * multiplier["player_attack"])
        player_defense = int(base_defense * multiplier["player_defense"])
        player_dodge = base_dodge

        equipped_weapon = items["меч_воина"]
        player_inventory.append(items["зелье_здоровья"])

    print(f"\nСоздан персонаж: {player_name} - {player_class}")
    print(f"Сложность: {game_difficulty}")
    show_player_stats()


def level_up():
    global player_level, player_exp, exp_to_next_level, player_stat_points, player_max_health, player_health

    while player_exp >= exp_to_next_level:
        player_level += 1
        player_exp -= exp_to_next_level
        exp_to_next_level = int(exp_to_next_level * 1.5)
        player_stat_points += 5
        player_max_health += 20
        player_health = player_max_health

        print()
        print("★" * 60)
        print(' ' * 24 + f"★ ДОСТИГНУТ УРОВЕНЬ {player_level}! ★")
        print("★" * 60)
        print("Ваше здоровье увеличено на 20 единиц!")
        print("Вы получили 5 очков характеристик!")

    distribute_stat_points()


def distribute_stat_points():
    global player_stat_points, player_max_health, player_health, player_attack, player_defense, player_dodge

    while player_stat_points > 0:
        show_player_stats()
        print(f"\nОсталось очков характеристик: {player_stat_points}")
        print("\t1: +10 к максимальному здоровью (также восстанавливает здоровье)")
        print("\t2: +5 к атаке (увеличивает наносимый урон)")
        print("\t3: +5 к защите (уменьшает получаемый урон)")
        print("\t4: +2% к уклонению (шанс избежать атаки врага)")
        print("\t5: Пропустить распределение (можно распределить позже)")

        choice = input("Выберите улучшение (1-5): ")

        if choice == "1":
            player_max_health += 10
            player_health += 10
            player_stat_points -= 1
            print("Максимальное здоровье увеличено на 10 единиц!")
        elif choice == "2":
            player_attack += 5
            player_stat_points -= 1
            print("Атака увеличена на 5 единиц!")
        elif choice == "3":
            player_defense += 5
            player_stat_points -= 1
            print("Защита увеличена на 5 единиц!")
        elif choice == "4":
            player_dodge += 2
            player_stat_points -= 1
            print("Уклонение увеличено на 2%!")
        elif choice == "5":
            print("Распределение очков отложено. Вы можете распределить их позже.")
            break
        else:
            print("Неверный выбор! Пожалуйста, выберите от 1 до 5.")


def add_exp(amount):
    global player_exp, player_level

    multiplier = difficulty_multipliers[game_difficulty]
    adjusted_amount = int(amount * multiplier["exp_gain"])

    player_exp += adjusted_amount
    print(f"Получено {adjusted_amount} опыта! (базовый опыт: {amount}, множитель сложности: {multiplier['exp_gain']}x)")

    if player_exp >= exp_to_next_level:
        level_up()


def add_gold(amount):
    global player_gold
    player_gold += amount
    print(f"Получено {amount} золота! 💰")


def use_item():
    while True:
        if not player_inventory:
            print("Ваш инвентарь пуст! Найдите предметы в сундуках")
            return False

        print("\n" + "-" * 40)
        print("\tИНВЕНТАРЬ")
        print("-" * 40)
        for i, item in enumerate(player_inventory, 1):
            print(f"\t{i}: {item['name']} - {item['description']}")
        print("-" * 40)
        print("\t0: Выйти")

        try:
            choice = int(input("Выберите предмет для использования: "))
            if choice == 0:
                return False
            elif 1 <= choice <= len(player_inventory):
                item = player_inventory[choice - 1]

                if item["type"] == "зелье":
                    if item["effect"] == "heal":
                        heal_amount = item["value"]
                        global player_health, player_max_health
                        player_health = min(player_max_health, player_health + heal_amount)
                        print(f"Использовано {item['name']}! Восстановлено {heal_amount} здоровья.")
                    elif item["effect"] == "attack":
                        global player_attack
                        player_attack += item["value"]
                        print(f"Использовано {item['name']}! Атака увеличена на {item['value']} до конца боя.")

                    player_inventory.remove(item)
                    return True
                else:
                    print(f"{item['name']} нельзя использовать напрямую. Это экипировка.")
                    return False
            else:
                print("Неверный выбор! Пожалуйста, выберите номер из списка.")
        except ValueError:
            print("Введите число, соответствующее номеру предмета!")


def equip_item():
    global equipped_weapon, equipped_armor

    if not player_inventory:
        print("Ваш инвентарь пуст! Найдите предметы в сундуках")
        return False

    print("\n" + "-" * 40)
    print("\tЭКИПИРОВКА ПРЕДМЕТОВ")
    print("-" * 40)
    for i, item in enumerate(player_inventory, 1):
        print(f"\t{i}: {item['name']} - {item['description']}")
    print("-" * 40)

    try:
        choice = int(input("Выберите предмет для экипировки (0 для отмены): "))
        if choice == 0:
            return False
        elif 1 <= choice <= len(player_inventory):
            item = player_inventory[choice - 1]

            if item["type"] == "оружие":
                if equipped_weapon:
                    player_inventory.append(equipped_weapon)
                    print(f"Снято: {equipped_weapon['name']}")
                equipped_weapon = item
                player_inventory.remove(item)
                print(f"Экипировано: {item['name']}")
                return True

            elif item["type"] == "броня":
                if equipped_armor:
                    player_inventory.append(equipped_armor)
                    print(f"Снято: {equipped_armor['name']}")
                equipped_armor = item
                player_inventory.remove(item)
                print(f"Экипировано: {item['name']}")
                return True
            else:
                print("Этот предмет нельзя экипировать!")
                return False
        else:
            print("Неверный выбор! Пожалуйста, выберите номер из списка.")
            return False
    except ValueError:
        print("Введите число, соответствующее номеру предмета!")
        return False


def calculate_damage():
    damage = get_total_attack() + random.randint(0, 5)
    if random.randint(1, 100) <= 10:
        damage = int(damage * 1.5)
        print("Критический удар! Урон увеличен на 50%!")
    return damage


def calculate_defense():
    return get_total_defense()


def player_attack_enemy(enemy):
    damage = calculate_damage() - enemy["defense"] // 2
    damage = max(1, damage)
    enemy["health"] -= damage
    print(f"Вы нанесли {damage} урона {enemy['name']}!")


def enemy_attack_player(enemy):
    if random.randint(1, 100) <= get_total_dodge():
        print("Вы увернулись от атаки врага!")
        return

    damage = enemy["attack"] - calculate_defense() // 2
    damage = max(1, damage)
    global player_health
    player_health -= damage
    print(f"{enemy['name']} наносит вам {damage} урона!")


def battle(enemy_index):
    global player_health, player_alive, player_gold

    enemy = get_enemy(enemy_index)
    second_phase_activated = False

    print("\n" + "⚔" * 35)
    print(f"\t⚔ БОЙ С {enemy['name'].upper()}! ⚔")
    print("⚔" * 35)
    print(f"Описание: {enemy['description']}")
    print(f"Сложность: {game_difficulty}")
    print("⚔" * 35)

    while player_health > 0 and enemy["health"] > 0:
        print(f"\nВаше здоровье: {player_health}/{player_max_health}")
        print(f"Здоровье {enemy['name']}: {enemy['health']}/{enemy['max_health']}")
        if (enemy_index == 4 and not second_phase_activated and
                enemy["health"] <= enemy["max_health"] * 0.5):

            print_slow("\nЧто-то изменилось... Воздух стал гуще, реальность искажается.")
            print_slow("Первозданный Хаос медленно поднимается, его форма начинает меняться.")
            print_slow("Ты чувствуешь, как дрожит само пространство вокруг.")
            time.sleep(1)

            print_slow("\nГолос из ниоткуда: 'Ты видел лишь тень моей силы...'")
            print_slow("'Пришло время показать тебе истинную сущность хаоса.'")
            time.sleep(2)

            try:
                if os.path.exists("WNM.mp3"):
                    print_slow("Звучит древняя мелодия, пробуждающая что-то первозданное...")
                    pygame.mixer.music.load("WNM.mp3")
                    pygame.mixer.music.play(-1)
                    music_started = True
                else:
                    print_slow("Эпическая музыка наполняет воздух...")
            except Exception as e:
                print(f"Не удалось воспроизвести музыку: {e}")
                print_slow("Звуковые вибрации меняются, становясь более интенсивными...")
            enemy["health"] = enemy["max_health"]
            enemy["attack"] = int(enemy["attack"] * 1.8)
            enemy["defense"] = int(enemy["defense"] * 1.5)
            enemy["name"] = "Пробужденный Первозданный Хаос"

            print_slow(f"\nХаос восстанавливается! Его сила многократно возрастает!")
            print_slow("Реальность вокруг начинает распадаться на части...")

            second_phase_activated = True
            time.sleep(2)

        print("\nВыберите действие:")
        print("\t1: Атаковать (стандартная атака)")
        print("\t2: Использовать предмет (восстановить здоровье или усилить характеристики)")
        print("\t3: Попытаться уклониться (шанс: {}%)".format(get_total_dodge()))
        print("\t4: Осмотреть противника (узнать характеристики врага)")

        choice = input("Ваш выбор (1-4): ")

        if choice == "1":
            player_attack_enemy(enemy)
        elif choice == "2":
            if use_item():
                continue
            else:
                continue
        elif choice == "3":
            dodge_success = random.randint(1, 100) <= get_total_dodge()
            if dodge_success:
                print("Вы приготовились уворачиваться от следующей атаки!")
                pass
            else:
                print("Вам не удалось сконцентрироваться для уклонения!")
        elif choice == "4":
            print(f"\nИнформация о {enemy['name']}:")
            print(f"\tЗдоровье: {enemy['health']}/{enemy['max_health']}")
            print(f"\tАтака: {enemy['attack']}")
            print(f"\tЗащита: {enemy['defense']}")
            if second_phase_activated:
                print(f"\tФаза: Вторая (пробужденная)")
                print(f"\tОпасность: Максимальная")
            print(f"\tОпыт за победу: {enemy['exp']}")
            print(f"\tЗолото за победу: {enemy['gold']}")
            continue
        else:
            print("Неверный выбор! Вы пропускаете ход.")

        if enemy["health"] <= 0:
            break

        print(f"\nХод {enemy['name']}...")
        time.sleep(1)

        if second_phase_activated and random.random() < 0.3:  # 30% шанс особой атаки
            attack_type = random.choice(["reality", "time", "chaos"])

            if attack_type == "reality":
                print_slow("🌀 Реальность искажается вокруг вас...")
                damage = enemy["attack"] + random.randint(10, 20)
                player_health -= damage
                print(f"Искажение реальности наносит {damage} урона!")

            elif attack_type == "time":
                print_slow("⏳ Время замедляется вокруг вас...")
                global player_dodge
                player_dodge = max(0, player_dodge - 15)
                print("Ваше уклонение уменьшено на 15%!")

            elif attack_type == "chaos":
                print_slow("💫 Хаос поглощает часть вашей силы...")
                heal_amount = random.randint(20, 40)
                enemy["health"] = min(enemy["max_health"], enemy["health"] + heal_amount)
                print(f"Хаос поглощает вашу энергию и восстанавливает {heal_amount} здоровья!")
        else:
            enemy_attack_player(enemy)

    if player_health <= 0:
        print("\nВы пали в бою...")
        player_alive = False
        return False
    else:
        if second_phase_activated:
            print_slow("\nТы сделал это... Ты победил непобедимое.")
            print_slow("Первозданный Хаос медленно рассеивается, оставляя после лишь тишину.")
            print_slow("Реальность постепенно возвращается к своему обычному состоянию.")
        else:
            print(f"\nПобеда! Вы победили {enemy['name']}!")

        add_exp(enemy["exp"])
        add_gold(enemy["gold"])
        return True


def shop():
    global player_gold, player_inventory

    while True:
        print("\n" + "=" * 20)
        print(" " * 5 + "= МАГАЗИН =")
        print("=" * 20)
        print("Добро пожаловать в магазин! Здесь вы можете купить полезные предметы.")
        print(f"Ваше золото: {player_gold} 💰")
        print("\nДоступные товары:")

        available_items = [
            ("зелье_здоровья", "Зелье здоровья (50 золота) - восстанавливает 50 HP"),
            ("зелье_силы", "Зелье силы (75 золота) - +10 к атаке до конца боя"),
            ("меч_воина", "Меч воина (200 золота) - +15 к атаке"),
            ("посох_мага", "Посох мага (300 золота) - +20 к атаке"),
            ("щит_защиты", "Щит защиты (250 золота) - +15 к защите"),
            ("эликсир_богов", "Эликсир богов (200 золота) - восстанавливает 200 HP"),
            ("плащ_теней", "Плащ теней (250 золота) - +10% к уклонению"),
            ("кольцо_могущества", "Кольцо могущества (400 золота) - +25 к атаке"),
            ("артефакт_хаоса", "Артефакт Хаоса (600 золота) - +40 к атаке")
        ]

        for i, (item_key, description) in enumerate(available_items, 1):
            print(f"\t{i}: {description}")

        print("\t0: Выйти из магазина")

        try:
            choice = int(input("\nВыберите товар для покупки (0-9): "))

            if choice == 0:
                break

            item_keys = [item[0] for item in available_items]
            if 1 <= choice <= len(item_keys):
                item_key = item_keys[choice - 1]
                item = items[item_key]

                if player_gold >= item["price"]:
                    player_gold -= item["price"]
                    player_inventory.append(item)
                    print(f"🏪 Вы купили {item['name']} за {item['price']} золота!")
                    print(f"🏪 Осталось золота: {player_gold} 💰")
                else:
                    print("Недостаточно золота!")
            else:
                print("Неверный выбор!")
        except ValueError:
            print("Введите число от 0 до 9!")


def open_chest(bonus=False):
    print("Вы нашли сундук с сокровищами!" if not bonus else "Вы нашли бонусный сундук!")

    owned_items = [item["name"] for item in player_inventory]
    if equipped_weapon:
        owned_items.append(equipped_weapon["name"])
    if equipped_armor:
        owned_items.append(equipped_armor["name"])

    item_keys = list(items.keys())
    available_items = [key for key in item_keys if items[key]["name"] not in owned_items]

    if not available_items:
        gold_found = random.randint(100, 300) if not bonus else random.randint(50, 150)
        print(f"В сундуке вы находите {gold_found} золота!")
        add_gold(gold_found)
        return

    random_item_key = random.choice(available_items)
    found_item = items[random_item_key]

    print(f"В сундуке вы находите: {found_item['name']}!")
    print(f"Описание: {found_item['description']}")
    player_inventory.append(found_item)
    gold_found = random.randint(50, 200) if not bonus else random.randint(25, 100)
    add_gold(gold_found)

    if found_item["type"] == "зелье":
        use_now = input("Использовать сейчас? (y/n): ").lower()
        if use_now == 'y' or use_now == 'д':
            if found_item["effect"] == "heal":
                heal_amount = found_item["value"]
                global player_health, player_max_health
                player_health = min(player_max_health, player_health + heal_amount)
                print(f"Использовано! Восстановлено {heal_amount} здоровья.")
                player_inventory.remove(found_item)


def explore_location():
    global current_location, player_health, player_max_health, location_visited, final_boss_defeated, hidden_boss_defeated

    location = locations[current_location]

    print("\n" + "=" * 80)
    print(f"\tЛОКАЦИЯ: {location['name']}")
    print("=" * 80)
    print(location['description'])
    print()

    if location["type"] == "скрытый бой" and game_difficulty != "невозможная":
        print("Эта локация доступна только на сложности 'Невозможная'!")
        return True

    bonus_chest = False
    if location_visited[current_location] and location["type"] not in ["отдых", "финальный бой", "скрытый бой"]:
        if random.random() < 0.3:
            bonus_chest = True
            print("При повторном осмотре вы находите бонусный сундук!")
            open_chest(bonus=True)
            return True
        else:
            print("Вы уже исследовали эту локацию. Здесь больше нечего делать.")
            return True

    location_visited[current_location] = True

    if location["type"] == "бой":
        if current_location == 0:
            enemy_index = 0
        elif current_location == 2:
            enemy_index = 1
        elif current_location == 4:
            enemy_index = 2
        else:
            enemy_index = min(current_location, len(base_enemies) - 2)

        return battle(enemy_index)

    elif location["type"] == "финальный бой":
        if final_boss_defeated:
            print("Вы уже победили Хроноса! Его поверженное тело все еще лежит здесь.")
            return True

        print_slow("Вы достигли Престола Хроноса!")
        print_slow("Перед вами предстал верховный бог времени - Хронос!")
        print_slow("Пришло время отомстить за всё!")
        time.sleep(2)

        boss_victory = battle(3)

        if boss_victory:
            final_boss_defeated = True

            if game_difficulty == "невозможная" and not hidden_boss_defeated:
                print()
                print("🌟" * 50)
                print(" " * 15 + "🌟 Открыта скрытая локация: Измерение Забвения! 🌟")
                print("🌟" * 50)
                print("Порталы в неизведанное измерение открылись перед вами!")
                print("Теперь вы можете отправиться туда из меню путешествия!")
                return True
            else:
                return "victory"
        else:
            return False

    elif location["type"] == "скрытый бой":
        if hidden_boss_defeated:
            print("Вы уже победили Первозданный Хаос! Его энергия рассеялась по вселенной.")
            return True

        print_slow("Вы вошли в Измерение Забвения!")
        print_slow("Перед вами предстал Первозданный Хаос - существо, существовавшее до рождения времени!")
        print_slow("Это ваш самый трудный бой...")
        time.sleep(2)

        hidden_boss_victory = battle(4)

        if hidden_boss_victory:
            hidden_boss_defeated = True
            return "hidden_victory"
        else:
            return False

    elif location["type"] == "сундук":
        open_chest()
        return True

    elif location["type"] == "отдых":
        print("Вы нашли место для отдыха.")
        heal_amount = player_max_health // 2
        player_health = min(player_max_health, player_health + heal_amount)
        print(f"Вы отдохнули и восстановили {heal_amount} здоровья!")
        show_player_stats()
        return True

    return True


def show_travel_options():
    global current_location

    while True:
        print()
        print("-" * 50)
        print("Куда вы хотите отправиться дальше?")
        print("-" * 50)

        available_locations = []

        if current_location < len(locations) - 1:
            next_loc = locations[current_location + 1]
            if next_loc["type"] == "скрытый бой" and game_difficulty != "невозможная":
                pass
            else:
                available_locations.append((1, next_loc))
                if next_loc["type"] == "скрытый бой":
                    print(f"\t1: Отправиться в Измерение Забвения - сразиться с Первозданным Хаосом!")
                else:
                    print(f"\t1: Отправиться вперед - в {next_loc['name']}")

        if current_location > 0:
            prev_loc = locations[current_location - 1]
            available_locations.append((2, prev_loc))
            print(f"\t2: Вернуться назад - в {prev_loc['name']}")
        print("\t3: Осмотреть текущую локацию еще раз")
        print("\t4: Посмотреть характеристики")
        print("\t5: Использовать предмет")
        print("\t6: Экипировать предмет")
        print("\t7: Распределить очки характеристик")
        print("\t8: Магазин (купить предметы за золото)")
        if game_difficulty == "невозможная" and final_boss_defeated and not hidden_boss_defeated and current_location != 6:
            print(f"\t9: Отправиться в Измерение Забвения - сразиться с Первозданным Хаосом!")
        print("\t0: Выйти из игры")

        choice = input("Ваш выбор: ")

        if choice == "1" and current_location < len(locations) - 1:
            next_loc = locations[current_location + 1]
            if next_loc["type"] == "скрытый бой" and game_difficulty != "невозможная":
                print("Эта локация доступна только на сложности 'Невозможная'!")
            else:
                current_location += 1
                break
        elif choice == "2" and current_location > 0:
            current_location -= 1
            break
        elif choice == "3":
            print("\nВы осматриваете локацию еще раз...")
            print(locations[current_location]['description'])
        elif choice == "4":
            show_player_stats()
        elif choice == "5":
            use_item()
        elif choice == "6":
            equip_item()
        elif choice == "7":
            if player_stat_points > 0:
                distribute_stat_points()
            else:
                print("У вас нет свободных очков характеристик для распределения.")
        elif choice == "8":
            shop()
        elif choice == "0":
            global game_running
            confirm = input("Вы уверены, что хотите выйти? (y/n): ").lower()
            if confirm == 'y' or confirm == 'д':
                print("Спасибо за игру! До свидания!")
                game_running = False
                break
        else:
            print("Неверный выбор! Пожалуйста, выберите доступный вариант.")


def game_loop():
    global game_running, player_alive, current_location, final_boss_defeated, hidden_boss_defeated

    print("\nНачинается ваше путешествие по Хроноспирали...")
    time.sleep(1)

    while game_running and player_alive:
        result = explore_location()

        if result == "victory":
            show_ending()
            break
        elif result == "hidden_victory":
            show_hidden_ending()
            break
        elif not result:
            break

        if final_boss_defeated and hidden_boss_defeated and game_difficulty == "невозможная":
            show_hidden_ending()
            break
        elif final_boss_defeated and game_difficulty != "невозможная":
            show_ending()
            break

        show_travel_options()

        time.sleep(1)


def show_ending():
    print("\n" + "★" * 38)
    print("\t" * 5 + "★ ПОБЕДА! ★")
    print("★" * 37)
    print_slow("\nВы стоите над поверженным телом Хроноса.")
    print_slow("Боги времени повержены. Их власть над вселенной разрушена.")
    print_slow("Вы отомстили за всё, что они сделали с вами и вашим народом.")
    print_slow("\nВремя начинает течь по-новому, свободное от тирании богов.")
    print_slow("Наконец-то, смертные обрели контроль над своей собственной судьбой.")
    print_slow("\nНо теперь перед вами стоит новый выбор...")
    print_slow("Стать новым богом времени или разрушить Хроноспираль навсегда?")
    print_slow("Оставить время свободным течь своим чередом или взять бразды правления в свои руки?")
    print_slow("\nКакой бы путь вы ни выбрали, ваше имя навсегда впишется в историю.")
    print_slow("В историю как имя того, кто бросил вызов богам и победил.")
    print_slow(f"\n{player_name}, вы вошли в легенду как спаситель вселенной!")
    print_slow("\nКонец игры.")
    print("★" * 38)


def show_hidden_ending():
    print()
    print("🌌" * 39)
    print(" " * 32 + "🌌 АБСОЛЮТНАЯ ПОБЕДА! 🌌")
    print("🌌" * 39)
    print()
    print_slow("Вы стоите над рассеивающейся сущностью Первозданного Хаоса.")
    print_slow("Вы победили не только богов времени, но и саму первозданную тьму.")
    print_slow("Ваше имя будет помнить не только эта вселенная, но и все измерения.")
    print()
    print_slow("Вы стали тем, кто определяет судьбу не просто миров, а самой реальности.")
    print_slow("Хроноспираль теперь под вашим контролем, и вы решаете, как будет течь время.")
    print()
    print_slow("Вы - новый Повелитель Времени и Хаоса.")
    print_slow("Ваша воля определяет законы мироздания.")
    print_slow("Ничто больше не угрожает существованию вселенной.")
    print()
    print_slow(f"{player_name}, вы стали легендой, которая будет жить вечно!")
    print()
    print_slow("Истинный конец игры.")
    print()
    print("🌌" * 39)


def show_game_over():
    print()
    print("=" * 80)
    print('\t' * 5 + "= ИГРА ОКОНЧЕНА =")
    print("=" * 80)
    print_slow("\nВаше путешествие по Хроноспирали завершилось.")
    print_slow("Вы пали в бою, но ваша жертва не будет забыта.")
    print_slow("Возможно, в другой раз удача будет на вашей стороне...")
    print_slow("\nПопробуйте сыграть снова с другим классом или стратегией!")
    print_slow("Или выберите другую сложность, чтобы испытать себя по-новому.")


def main():
    show_title()
    show_intro()
    choose_difficulty()
    create_character()

    input("\nНажмите Enter чтобы начать ваше путешествие...")

    game_loop()

    if not player_alive:
        show_game_over()

    print("\nСпасибо за игру в ХРОНОСПИРАЛЬ!")
    input("\nНажмите любую клавишу чтобы выйти...")


if __name__ == "__main__":
    main()