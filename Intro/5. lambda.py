# Лямбда-вирази: вирази, результатом яких є функціїї

def oper (lam) -> int:
    return lam(1,2)

def main() -> None:
    lam1 = lambda x : print(x) # x => print(x)
    lam1('Hello')
    lam2 = lambda x, y : print(x, y) # (x, y) => ...
    lam2('Hello', 'World')
    lam3 = lambda:print('No args') # () => ...
    lam3()
    # економія пам'яті "одноразові функції" - після виконання не лишаються у пам'яті
    (lambda:print(10))() # IIFE - immediately invoked func expression
    # передача дії (функції) до іншої функції (~ паттерн "Стратегія")
    print("Sum: ", oper(lambda x, y: x+y))
    print("Dif: ", oper(lambda x, y: x-y))

if __name__ == '__main__':
    main()
