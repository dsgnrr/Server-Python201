'''
Д.З. Описати клас "дріб" (чисельник, знаменник - цілі числа)
Реалізувати можливість конструювати дроби без параметрів ( 0/1 ),
з одним параметром ( 10/1 ) та з двома параметрами ( 2/3 )
Забезпечити відображення об'єктів у формі "(2/3)"
Реалізувати метод для скорочення дробу (12/15).reduce() -> (4/5)
Створити декілька об'єктів (різним способом), демонструвати
виведення та роботу reduce()
* Встановити сервер Apache та СУБД MySQL/MariaDb (можна у збірці типу XAMPP)
'''


class Fraction:
    numer:int
    denom:int

    def __init__(self,numer=0, denom=1):
        self.numer=numer
        self.denom=denom

    def __str__(self) -> str:
        return "(%d/%d)" % (self.numer,self.denom)
    
    def reduce(self):
        isReduce=False
        for val in range(2,10):
            if self.numer%val==0 and self.denom%val==0:
                self.numer/=val
                self.denom/=val
                break
            if self.numer<val or self.denom<val:
                isReduce=True
        if isReduce:
            return
        else:
            self.reduce()

def main()->None:
    frac1 = Fraction()
    print("Fraction1(without params): %s" %(frac1))
    print('---------------------------------------')
    frac2 = Fraction(denom=3)
    print("Fraction2(denominator=3): %s" %(frac2))
    print('---------------------------------------')
    frac3 = Fraction(numer=5)
    print("Fraction3(numerator=5): %s" %(frac3))
    print('---------------------------------------')
    frac4 = Fraction(12,15)
    print("Fraction4(12,15): %s" %(frac4))
    frac4.reduce()
    print("Fraction4 after reduce: %s" %(frac4))
    print('---------------------------------------')
    pass

if __name__=="__main__":
    main()