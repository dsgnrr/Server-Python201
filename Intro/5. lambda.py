# Лямбда-вирази: вирази, результатом яких є функціїї
import math
import random
def oper (lam) -> int:
    return lam(1,2)

def homework(val1,val2):
    if val1 <= 0 or val2 <= 0:
        print('Error! Values must be long than zero')
        return
    
    lambda_list=[
        lambda x,y: (x+y)/2,
        lambda x,y: math.sqrt(x*y),
        lambda x,y: 2.0 * (x * y) / (x + y)
    ]

    results = []
    
    for lam in lambda_list:
        res=lam(val1, val2)
        results.append(res)

    strategies=["Arifmetic","Geometric","Harmonic"]
    strateg_index = 0
    min=results[0]
    for res in results:
        if(min > res):
            min = res
            strateg_index+=1
        
    print(strategies[strateg_index],": ",min)
   
        

def main() -> None:
   homework(random.uniform(1,100),random.uniform(1,100))
    # lam1 = lambda x : print(x) # x => print(x)
    # lam1('Hello')
    # lam2 = lambda x, y : print(x, y) # (x, y) => ...
    # lam2('Hello', 'World')
    # lam3 = lambda:print('No args') # () => ...
    # lam3()
    # # економія пам'яті "одноразові функції" - після виконання не лишаються у пам'яті
    # (lambda:print(10))() # IIFE - immediately invoked func expression
    # # передача дії (функції) до іншої функції (~ паттерн "Стратегія")
    # print("Sum: ", oper(lambda x, y: x+y))
    # print("Dif: ", oper(lambda x, y: x-y))

if __name__ == '__main__':
    main()
