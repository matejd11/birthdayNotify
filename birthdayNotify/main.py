from birthdayNotify.personDb import PersonDb
from birthdayNotify.shell import Shell
import argparse
import sys


def main(shell = True):
    if shell:
        shell = Shell("skuska")
        shell.go()
    else:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BirthdayNotify')
    parser.add_argument("--shell", action='store_true', default=False)

    result = parser.parse_args()

    main(result.shell)
