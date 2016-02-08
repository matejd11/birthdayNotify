from birthdayNotify.personDb import PersonDb
from birthdayNotify.shell import Shell
import argparse
import sys

def some(*, shell):
    if shell:
        shell = Shell("skuska")
        shell.go()
    else:
        pass

def main():
    parser = argparse.ArgumentParser(description='BirthdayNotify')
    parser.add_argument("--shell", action='store_true', default=False)

    result = parser.parse_args()

    some(shell = result.shell)

if __name__ == '__main__':
    main()
