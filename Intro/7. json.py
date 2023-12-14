# робота з JSON
import json # модуль з "коробки" для роботи з JSON

def main() -> None:
    try:
        with open("sample.json") as f:
            j = json.load(f)
    except :
        print("JSON load error: ")
        return

    print(type(j),j) # <class 'dict'> {'d': 123, 'f': 12.34...

    for k in j:
        print(k, j[k], type(j[k]))
    
    j['newItem1']='Hi, All'
    j['newItem2']='Вітання'
    print(j)            # ...'newItem2': 'Вітання'}
    print(json.dumps(j))# ..."newItem2": "\u0412\u0456\u0442\u0430\u043d\u043d\u044f"}
    print(json.dumps(j, #
                     ensure_ascii=False, # не екранувати Unicode('newItem2':'Вітання') 
                     indent=4)) # pretty print (відступ 4 пробіли)
    
    # Перевірити, чи є ключ "arr" у json
    key="r2d2"
    if key in j:
        print(key,"exists")
    else:
        print(key,"does not exist")
    
    try:
        with open("sample2.json","w", encoding="utf-8") as f:
            json.dump(j,f,ensure_ascii=False, indent=4)
    except:
        print("Write fail")
    else:
        print("Write OK")
    pass

if __name__ == "__main__":
    main()