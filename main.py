import test
import lab1
import lab2
import lab3
import lab4
import lab5
import lab6
import lab7
import lab8
import lab9


if __name__ == '__main__':
    switch = input('Choose lab: ')
    if switch == '1':
        lab1.main()
    elif switch == '2':
        lab2.main()
    elif switch == '3':
        lab3.main()
    elif switch == '4':
        lab4.main()
    elif switch == '5':
        lab5.main()
    elif switch == '6':
        lab6.main()
    elif switch == '7':
        lab7.main()
    elif switch == '8':
        lab8.main()
    elif switch == '9':
        lab9.main()
    else:
        test.main()
