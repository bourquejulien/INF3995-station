#!/usr/bin/env python

import black
import sys


def format():
    black.main(["."])


def show_diff():
    black.main(["--diff", "--check", "."])


def main(param: list):
    if len(param) > 0 and param[0] == "--fix":
        format()
        return
    show_diff()


if __name__ == "__main__":
    main(sys.argv[1:])
