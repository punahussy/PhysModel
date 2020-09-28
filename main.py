from emulator import emulate
from scipy import constants as constants
from visualizer import visualize

VISUAL_DEBUG = True

class Case:
    def __init__(self, m1, m2, v1):
        self.m1 = m1
        self.m2 = m2
        self.v1 = v1


cases = [
    Case(20, 40, 5),
    Case(50, 10, 10),
    Case(1, 25, constants.speed_of_sound),
    Case(400, 25, 10),
    Case(10, 25, 100000000000000000),
    Case(0, 9, 1,),
    Case(10, 0, 500)
]


currentCase = Case(10, 1, 20)


def manual_input():
    m1 = float(input("Масса ядра: "))
    m2 = float(input("Масса ящика: "))
    v = float(input("Начальная скорость: "))
    global currentCase
    if emulate(m1, m2, v):
        currentCase = Case(m1, m2, v)


def run_test_cases():
    case_number = 1
    for case in cases:
        print("\n=====Тестовый случай #{} ====".format(case_number))
        m1 = case.m1
        m2 = case.m2
        v = case.v1
        print(" Масса ядра: {0} кг. \n Масса ящика: {1} кг. \n Скорость ядра: {2} м/c.".format(m1, m2, v))
        emulate(m1, m2, v)
        case_number += 1


def console():
    print("Введите команду:")
    command = input("tests - Запутстить тестовые случаи. \nmanual - Ввести данные вручную \nquit - выйти\n").lower()
    while command != "q":
        if command == "":
            command = input().lower()
            continue
        elif command[0] == "t":
            print("Запуск тестов")
            run_test_cases()
        elif command[0] == "m":
            manual_input()
        elif command[0] == "v":
            visualize(currentCase.m1, currentCase.m2, currentCase.v1)
        else:
            print("Команда не опознана")
        command = input().lower()


print("=====РАСЧЕТ ПО МАТЕМАТИЧЕСКОЙ МОДЕЛИ====")
print("Формулировка задачи:")
print(" Из пушки, расположенной под углом в 45° стреляют ядром с массой m1 и начальной скоростью v. \n"
      "Ядро попадает в ящик, наполненный идеально неупругим материалом, с массой m2,\nпосле чего ящик вместе с ядром "
      "проезжает расстояние S, "
      " прежде чем полностью остановится под силой трения.\n"
      "В зависимости от входных данных рассчитывается пройденное ящиком расстояние.\n")
print("Тушнолобов Е. Пономарев А. \nРИ-380014, 2020\n")
if not VISUAL_DEBUG:
    console()
else:
    visualize(currentCase.m1, currentCase.m2, currentCase.v1)
