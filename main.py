from personDb import PersonDb
import shell


def main():
    data = PersonDb('skuska')
    shell.go(data)

if __name__ == '__main__':
    main()
