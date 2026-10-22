#Варіант 49. Склад сувенірів
#Завдання 2. Розподіл записів за оцінкою
#Завдання майже однакові то більшість коду скопіював з першого але все змінював що треба було по умові завдання і додавав нового
import sys


class Item:  # батько
    def __init__(self, item_type, value, item_id):#item_type наприклад це А і В а value значення яке будемо задавати, item_id номер команди ADD
        # просто звернення щоб могли звернутися потім
        self.type = item_type
        self.value = value
        self.id = item_id

    def get_score(self):
        raise NotImplementedError#якщо викличемо через батьківський клас


# Два типа А і В які будуть виводити значення по завданню
class ItemA(Item):#наслідування
    def get_score(self):
        return 4 * self.value


class ItemB(Item):#наслідування
    def get_score(self):
        return 3 * self.value + 9


# клас Стек
class Stack:
    def __init__(self, capacity=3):#по завданню 2 місткість 3
        self.capacity = capacity
        self.items = []#створює порожній список

    def is_empty(self):
        return len(self.items) == 0#як раз перевіряє чи порожньо в списку

    def is_full(self):
        return len(self.items) >= self.capacity

    def push(self, item):
        if not self.is_full():
            self.items.append(item)#за допомогою аппенд додаємо елемент в кінець списку
            return True
        return False

    def pop(self):
        if not self.is_empty():
            return self.items.pop()#вилучає і повертає останній елемент
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]#просто перегляд останнього елементу
        return None

    def get_sum(self):
        return sum(item.get_score() for item in self.items)#іде отримання всіх оцінок з списку

    def get_log(self):
        if self.is_empty():
            return "-"#як раз по завданню якщо порожньо то буде повертати -
        return " ".join(str(item.id) for item in reversed(self.items))#а це формує список через джойн гарненько і також робить так щоб список ішов навпаки від кінця до початку


class Queue:
    def __init__(self, capacity=3):#по завданню місткість 3
        self.capacity = capacity#запамятовує
        self.items = []#і створює порожній список

    def is_empty(self):
        return len(self.items) == 0#те саме що і в попередньому

    def is_full(self):
        return len(self.items) >= self.capacity#перевіряє чи є ще місця в списку

    def enqueue(self, item):
        if not self.is_full():
            self.items.append(item)#якщо список не повний то додає ще один елемент в кінець списку
            return True
        return False

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)#навпаки перевірка іде на порожність якщо не порожня то видаляє та повертає перший елемент зі списку
        return None

    def get_sum(self):
        return sum(item.get_score() for item in self.items)#іде розрахунок як і в класі стек але тепер для класу черги

    def get_log(self):
        if self.is_empty():
            return "-"
        return " ".join(str(item.id) for item in self.items)#іде виписання так само як в класі стек але для класу черги


# Функція перевіряє клас до якого звертаються якщо стек то виконується функція поп а якщо черга то декюю
def polymorph_pop(structure):
    if isinstance(structure, Stack):
        return structure.pop()
    elif isinstance(structure, Queue):
        return structure.dequeue()
    return None


class all_system:
    def __init__(self):
        # створюю обєкти як приклади до них можна буде звертатися навіть в цьому класі
        self.s = Stack(3)
        self.q = Queue(3)
        # списки куди були вилучені записи
        self.log_taken_s = []
        self.log_taken_q = []
        # лічильники спроб
        self.counter_accepted_s = 0
        self.counter_accepted_q = 0
        self.counter_empty_s = 0
        self.counter_empty_q = 0
        self.counter_rejected_s = 0
        self.counter_rejected_q = 0
        # рахування порядкового номеру ADD
        self.command_id_counter = 0

    #Робить все те саме що і в першому завданні
    def process_command(self, command_line):
        parts = command_line.split()
        if not parts:
            return True
        cmd = parts[0]

        try:
            #Робить все теж саме що і в першому завданні
            if cmd == "ADD":
                if len(parts) < 3:
                    raise ValueError("Недостатньо аргументів для команди ADD.")
                item_type = parts[1]
                if item_type not in ("А", "A", "В", "B"):
                    raise ValueError(f"Невідомий тип елемента: '{item_type}'. Дозволені: A, B.")

                value = int(parts[2])
                if not (0 <= value <= 1000):
                    raise ValueError(f"Значення {value} поза діапазоном від 0 до 1000.")

                self.command_id_counter += 1
                normalized_type = "A" if item_type in ("А", "A") else "B"

                if normalized_type == "A":
                    new_item = ItemA(normalized_type, value, self.command_id_counter)
                else:
                    new_item = ItemB(normalized_type, value, self.command_id_counter)
                # тепер іде перевірка на вписання відхилених або прийнятих айді. Той самий спосіб як і в першому але тепер трохи по іншому із-за умови
                #ADD спрямовує запис з оцінкою не більшою за 32 до S , збільшою оцінкою — до Q
                score = new_item.get_score()
                if score <= 32:
                    if self.s.push(new_item):
                        self.counter_accepted_s += 1
                    else:
                        self.counter_rejected_s += 1
                else:
                    if self.q.enqueue(new_item):
                        self.counter_accepted_q += 1
                    else:
                        self.counter_rejected_q += 1
            #Тепер майже така ж сама перевірка для тейк оскільки нова умова по завданню
            elif cmd == "TAKE":
                if len(parts) < 3:
                    raise ValueError("Недостатньо аргументів для TAKE.")
                target = parts[1]
                if target not in ("S", "Q"):
                    raise ValueError(f"Невідоме сховище: '{target}'. Дозволені: S, Q.")

                k = int(parts[2])
                if not (0 <= k <= 20):
                    raise ValueError(f"k = {k} поза діапазоном від 0 до 20.")
                # Тут іде функція удаляє кінцеві результати і взагалі перевіряється чи пороожньо в класах стек і черга. Іде також збільшлення лічильника
                if target == "S":
                    for _ in range(k):
                        item = polymorph_pop(self.s)
                        if item is None:
                            self.counter_empty_s += 1
                        else:
                            self.log_taken_s.append(item.id)
                elif target == "Q":
                    for _ in range(k):
                        item = polymorph_pop(self.q)
                        if item is None:
                            self.counter_empty_q += 1
                        else:
                            self.log_taken_q.append(item.id)
            else:
                raise ValueError(f"Невідома команда: '{cmd}'.")

            return True
        # Завдяки цьому якщо виникне помилка то введеня не завершиться і тут як раз я використвоую import sys для леншого зчитвування помилок
        except ValueError as e:
            print(f"[ПОМИЛКА]: {e}", file=sys.stderr)
            print("Повторіть спробу введення цієї команди знову:", file=sys.stderr)
            return False

    # Іде виведення результатів, а ось за допомгою джойн прибирає всі розділові знаки і робить все через пробіл. За очікуваним результатом
    def print_results(self):
        taken_s_str = " ".join(map(str, self.log_taken_s)) if self.log_taken_s else "-"
        taken_q_str = " ".join(map(str, self.log_taken_q)) if self.log_taken_q else "-"

        print(f"S: {self.s.get_log()}")
        print(f"Q: {self.q.get_log()}")
        print(f"Сума S: {self.s.get_sum()}")
        print(f"Сума Q: {self.q.get_sum()}")
        print(f"Вилучено S: {taken_s_str}")
        print(f"Вилучено Q: {taken_q_str}")
        print(f"Прийнято S: {self.counter_accepted_s}")
        print(f"Прийнято Q: {self.counter_accepted_q}")
        print(f"Порожньо S: {self.counter_empty_s}")
        print(f"Порожньо Q: {self.counter_empty_q}")
        print(f"Відхилено S: {self.counter_rejected_s}")
        print(f"Відхилено Q: {self.counter_rejected_q}")

#така сама перевірка вписання кількості рядків і перевірка помилок якщо виходить за діапазон або введення не цілого числа.  Як і в першому завданні
#І перевірка на успішність вводу
def main():
    while True:
        try:
            first_line = input()
            if not first_line.strip():
                continue
            n = int(first_line.strip())
            if not (0 <= n <= 200):
                print("Помилка: n має бути в діапозоні від 0 до 200. Повторіть спробу введіть n:")
                continue
            break
        except ValueError:
            print("Помилка: введено не ціле число для n. Повторіть спробу:")

    system = all_system()

    processed_commands = 0
    while processed_commands < n:
        try:
            line = input()
            if not line.strip():
                continue

            success = system.process_command(line.strip())
            if success:
                processed_commands += 1
            else:
                print("Введіть правильну команду замість помилкової:")
        except (EOFError, KeyboardInterrupt):
            break

    system.print_results()


if __name__ == "__main__":
    main()