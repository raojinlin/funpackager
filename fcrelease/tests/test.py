import dis
import threading

from utils import timer


def countdown(n):
    while n > 0:
        n -= 1


@timer('sequence execution')
def seq():
    countdown(100000000)
    countdown(100000000)


@timer('main multi threads')
def main():
    # dis.dis(countdown)
    t1 = threading.Thread(target=countdown, args=(100000000,))
    t1.start()
    t2 = threading.Thread(target=countdown, args=(100000000,))
    t2.start()
    t1.join();t2.join()


class B:
    def __init__(self):
        print('B init')


class A(B):
    def __init__(self):
        B.__init__(self)
        print('A init')


class D:
    def __init__(self):
        # B.__init__(self)
        print('D init')
        self.d = 123


class C(A, D):
    def __init__(self):
        super(A).__init__()
        super(D).__init__()


if __name__ == '__main__':
    # main()
    seq()
    main()
