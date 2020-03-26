# encoding: utf-8

import time


def get_indent_spaces(indent=4, level=1):
    return ' ' * indent * level


def timer(name):
    def wrap(fc):
        def wrap1(*args, **kwargs):
            start = time.time()
            fc(*args, **kwargs)
            print("timer '%s' use time: %.2fs" % (name, time.time() - start))
        return wrap1
    return wrap

