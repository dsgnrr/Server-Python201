# Функції
x = 10

def pair():     # def - ключове слово для оглошення функції
    return x, 2  # повернення значення (кортеж)
                # Рекомендація - залишати щонайменше
                # два порожні рядки
def hello() -> str:         # Опціональне зазначення типу повернення ф-ції
    x = 20 # Локальна змінна, яка "перекриває" глобальну
    return "Hello, World %d" % (x)   # виведе 20, але глобальна змінна не зміниться


def change_x() -> None:
    global x # декларація того, що під "x" розуміється саме
    x = 20 # глобальна змінна, її нове значення зафіксується

def printPair(x, y):
    # str = "x = %d, y =%d" % (x, y)
    str = "x = %d, y =%d" % pair()
    print(str)


def homework():
    val1 = 0
    val2 = 0
    isValid = False
    while True:
        if isValid == False:
            val1 = input("Введіть х: ")
            val1 = int(val1)
            if val1 < 0:
                print("Потрібно додатнє число")
                continue
            else:
                isValid=True
                
        val2 = input("Введіть y: ")
        val2 = int(val2)
        if val2 < 0:
            print("Потрібно додатнє число")
            continue
        elif val2 == val1:
            print("Числа повинні відрізнятись")
            continue
        else:
            break
    print("%d + %d = %d" % (val1, val2, val1+val2))

def main() -> None:
    print(hello())
    x,y = pair()
    printPair(x, y) # 10 -- ілюстрація того, що х=20 не змінило глобальну змінну
    change_x()
    x,y = pair() 
    printPair(x, y) # 20 -- ілюстрація зміни глобальної "x"
    # homework()
    

# Одне з використань функцій - створення "точки входження"
# це корисне для впровадження інжектування, а також для
# розрізнення підключення файлу, як модуля, та його запуску, як
# головної програми
if __name__ == '__main__' : main() 