# Робота з файлами

def create_file1() -> None:
    fname = "file1.txt"
    f = None
    try:
        f = open(fname, mode="w",encoding="utf-8")
        f.write("Test file 1")
        f.write("\nNext line in file 1")
    except OSError as err:
        print("File 1 creation error", err)
    else:
        f.flush()
        print(fname, "created successfully")
    finally:
        if f != None : f.close()


def main() -> None:
    create_file1()


if __name__ == "__main__":
    main();