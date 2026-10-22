#Варіант 49. Склад сувенірів
#Завдання 1. Контроль оцінок і виправлення записів
import sys
import sys


class Item:#батько
    def __init__(self, item_type, value, item_id):#item_type - наприклад це А і В а value - значення яке будемо задавати, item_id- номер команди ADD
        #просто звернення щоб могли звернутися потім
        self.type = item_type
        self.value = value
        self.id = item_id

    def get_score(self):
        raise NotImplementedError#якщо викличемо через батьківський клас


# Два типа А і В які будуть виводити значення по завданню
class ItemA(Item):#наслідування
    def get_score(self):
        return 3 * self.value


class ItemB(Item):#наслідування
    def get_score(self):
        return 5 * self.value + 8


# клас Стек
class Stack:
    def __init__(self):
        self.items = []#створює порожній список

    def is_empty(self):
        return len(self.items) == 0  # як раз перевіряє чи порожньо в списку

    def push(self, item):
        self.items.append(item)#за допомогою аппенд додаємо елемент в кінець списку

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
        return " ".join(str(item.id) for item in reversed(self.items))#а це формує список через джойн через пробіли без розділових знаків і також робить так щоб список ішов навпаки від кінця до початку

#клас черги
class Queue:
    def __init__(self, capacity=5):#по завданню місткість 5
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


#Функція перевіряє клас до якого звертаються якщо стек то виконується функція поп а якщо черга то декюю
def polymorph_pop(structure):
    if isinstance(structure, Stack):
        return structure.pop()
    elif isinstance(structure, Queue):
        return structure.dequeue()
    return None


class all_system:
    def __init__(self):
        #створюю обєкти як приклади до них можна буде звертатися навіть в цьому класі
        self.s = Stack()
        self.q = Queue(5)
        #списки куди були прийняті відкладені чи повернуті
        self.log_accepted = []
        self.log_postponed = []
        self.log_returned = []
        #невдалі спроби
        self.counter_empty_q = 0
        self.counter_empty_s = 0
        self.counter_blocked = 0
        self.counter_rejected = 0
        #рахування порядкового номеру ADD
        self.command_id_counter = 0

    def process_command(self, command_line):
        parts = command_line.split()#приймає один рядок і розбиває його у список parts
        if not parts:
            return True
        cmd = parts[0]
        #за допомогою трай буде легше працювати з помилками
        try:
            #перівірка чи достатньо аргументів і чи правильний тип елемента
            if cmd == "ADD":
                if len(parts) < 3:
                    raise ValueError("Недостатньо аргументів для команди ADD.")
                item_type = parts[1]
                if item_type not in ("А", "A", "В", "B"):
                    raise ValueError(f"Невідомий тип елемента: '{item_type}'. Дозволені: A, B.")
                #перевіряє діпазон
                value = int(parts[2])
                if not (0 <= value <= 1000):
                    raise ValueError(f"Значення {value} поза діапазоном від 0 до 1000.")
                #збільшує лічильник на один створює відповідний клас А або В
                self.command_id_counter += 1
                normalized_type = "A" if item_type in ("А", "A") else "B"

                if normalized_type == "A":
                    new_item = ItemA(normalized_type, value, self.command_id_counter)
                else:
                    new_item = ItemB(normalized_type, value, self.command_id_counter)
                #іде звернення до класу черги і функції переповнення
                if not self.q.enqueue(new_item):
                    self.counter_rejected += 1
            #Тепер такаж сама перевірка для чек
            elif cmd == "CHECK":
                if len(parts) < 2:
                    raise ValueError("Недостатньо аргументів для CHECK.")
                k = int(parts[1])
                if not (0 <= k <= 20):
                    raise ValueError(f"k = {k} поза діапазоном від 0 до 20.")
                #цикл спроб вилучення з черги за допомогою polymorph_pop
                for _ in range(k):
                    head_item = polymorph_pop(self.q)
                    if head_item is None:
                        self.counter_empty_q += 1
                    else:
                        #тепер іде перевірка на вписання відхилених або прийнятих айді
                        if head_item.get_score() <= 21:
                            self.log_accepted.append(head_item.id)
                        else:
                            self.log_postponed.append(head_item.id)
                            self.s.push(head_item)
            #Таж сама перевірка для фікс
            elif cmd == "FIX":
                if len(parts) < 2:
                    raise ValueError("Недостатньо аргументів для FIX. Потрібно: FIX [x].")
                x = int(parts[1])
                if not (0 <= x <= 1000):
                    raise ValueError(f"x = {x} поза діапазоном від 0 до 1000.")
                #чисто дивимося на останній елемент
                top_item = self.s.peek()
                if top_item is None:#якщо цього елементу немає збільшуємо лічильник порожнечі
                    self.counter_empty_s += 1
                else:
                    #якщо є
                    top_item.value = x
            #така сама перевірка але для рековер
            elif cmd == "RECOVER":
                if len(parts) < 2:
                    raise ValueError("недостатньо аргументів для RECOVER.")
                k = int(parts[1])
                if not (0 <= k <= 20):
                    raise ValueError(f"k = {k} поза діапазоном від 0 до 20.")
                #цикл спочатку бере елмент зі стека
                for _ in range(k):
                    top_item = polymorph_pop(self.s)
                    if top_item is None:
                        #якщо порожній збільшує на один
                        self.counter_empty_s += 1
                    elif self.q.is_full():
                        #якщо повний
                        self.counter_blocked += 1
                        self.s.push(top_item)
                    else:
                        #якщо список не повний додає ще один елемент
                        self.q.enqueue(top_item)
                        self.log_returned.append(top_item.id)
            else:
                raise ValueError(f"Невідома команда: '{cmd}'.")

            return True
        #Завдяки цьому якщо виникне помилка то введеня не завершиться і тут як раз я використвоую import sys для леншого зчитвування помилок
        except ValueError as e:
            print(f"Помилка: {e}", file=sys.stderr)
            print("Повторіть спробу знову:", file=sys.stderr)
            return False

    #Іде виведення результатів, а ось за допомгою джойн прибирає всі розділові знаки і робить все через пробіл. За очікуваним результатом
    def print_results(self):
        accepted_str = " ".join(map(str, self.log_accepted)) if self.log_accepted else "-"
        postponed_str = " ".join(map(str, self.log_postponed)) if self.log_postponed else "-"
        returned_str = " ".join(map(str, self.log_returned)) if self.log_returned else "-"

        print(f"S: {self.s.get_log()}")
        print(f"Q: {self.q.get_log()}")
        print(f"Сума S: {self.s.get_sum()}")
        print(f"Сума Q: {self.q.get_sum()}")
        print(f"Прийнято: {accepted_str}")
        print(f"Відкладено: {postponed_str}")
        print(f"Повернено: {returned_str}")
        print(f"Порожньо Q: {self.counter_empty_q}")
        print(f"Порожньо S: {self.counter_empty_s}")
        print(f"Заблоковано: {self.counter_blocked}")
        print(f"Відхилено: {self.counter_rejected}")


def main():
    while True:
        try:
            #іде вписання кількості рядків і перевірка помилок якщо виходить за діапазон або введення не цілого числа
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

    system = all_system()#створення головного обєкту

    processed_commands = 0#лічильник для перевірки скільки вже успішних команд введено
    while processed_commands < n:#іде введеня кожного нового рядка поки менше заданого числа
        try:
            line = input()
            if not line.strip():
                continue

            success = system.process_command(line.strip())#якщо все пройшло то збільшує лічильник на один
            if success:
                processed_commands += 1
            else:
                print("Введіть правильну команду замість помилкової:")
        except (EOFError, KeyboardInterrupt):
            break

    system.print_results()#фінальний результат


if __name__ == "__main__":
    main()