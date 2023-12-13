# Виключні ситуації
def throw() -> None:
    print('Raising TypeError...')
    raise TypeError # аналог throw - створення виключної ситуації


def throw_with_message() -> None:
    print('Raising ValueError...')
    raise ValueError("ValueError message") # аналог throw - створення виключної ситуації


def main() -> None:
    try:
        # throw()
        # throw_with_message()
        pass
    except ValueError as err:
        print("Got message '%s'" % (err))
    except:
        print('Exception detected') # продовження try - якщо не було виключень
    else:
        print("Else action")
    finally:
        print("Finally action")

    pass # No operation - аналог порожнього тіла {}


if __name__ == '__main__': main()