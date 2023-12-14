# Робота з файлами

def create_file1() -> None:
    fname = "file1.txt"
    f = None
    try:
        f = open(fname, mode="w",encoding="utf-8")
        f.write("Test file 1")
        f.write("\nNext line in file 1")
        f.write("\nРядок з кириліцею")
    except OSError as err:
        print("File 1 creation error", err)
    else:
        f.flush()
        print(fname, "created successfully")
    finally:
        if f != None : f.close()


# Приклад з автозакриттям ресурсів
def create_file2()-> None:
    fname="file2.txt"
    try:
        with open(fname, mode="w",encoding="utf-8") as f: # ~ using (C#)
            f.write("Host: localhost\r\n")
            f.write("Connection: close\r\n")
            f.write("Content-Type: text/html")
    except OSError as err:
        print("File 2 creation error", err)


def read_all_text1(fname) -> str | None: 
    f = None
    try:
        f = open(fname, mode="r",encoding="utf-8")
        return f.read()
    except OSError as err:
        print("Read file error: ", err)
    finally:
        if f != None:
            f.close()


def read_all_text(fname) -> str | None: 
    try:
        with open(fname, mode="r",encoding="utf-8") as f:
            return f.read()
    except OSError as err:
        print("Read file error: ", err)
    # блок закриття не потрібен, оскільки "with" закриває автоматично


def read_lines(fname):
    try:
        with open(fname, mode="r",encoding="utf-8") as f:
            # i = 0
            # for line in f:            # ітерування файлу здійснюється по рядках (\n)
            #     print(f"{i}. {line}") # причому символ \n залишається у "line"
            #     i += 1
            return (line for line in f.readlines())
    except OSError as err:
        print("Read file error: ", err)


def parse_headers(fname)-> dict | None:
    try:
        with open(fname, mode="r",encoding="utf-8") as f:
            i = 0
            res = {}
            for line in f:
                parts = line.split(":")
                if len(parts) ==2:
                    res[parts[0]]=parts[1]
            if len(res)>0:
                return res
            else:
                return None            
    except OSError as err:
        print("Read file error: ", err)


def parse_headers2(fname)-> dict:
    ret = {}
    for line in read_lines(fname):
        if ':' in line:
            k,v=map(str.strip,line.split(':'))
            ret[k]=v
    return ret


def parse_headers3(fname) -> dict:
    return{                               # { - ознака dict (генератор словника)                  
        k: v for k,v in                   # правило генерування (k: v) for ..множина                               
        (map(str.strip, line.split(':'))   # оброблена str.strip пара line.split(':') по множині               
            for line in read_lines(fname) #  | множмна рядків фільтрована умовою                   
                if ':' in line)}          #  | if ':' in line     


def main() -> None:
    create_file2()
    # print(read_all_text("file2.txt"))
    # print(parse_headers("file2.txt"))
    n=1
    # for line in read_lines("file2.txt"):
    #     print(n,line)
    #     n+=1
    print(parse_headers2("file2.txt"))
    i=0
    for k,v in parse_headers3("file2.txt").items():
        i+=1
        print("%d. %s: %s" % (i,k,v))
        


if __name__ == "__main__":
    main();