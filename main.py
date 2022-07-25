import sys
from runner import run

def main():
    if len(sys.argv) != 2:
        print("Usage: {} <hexdata>".format(sys.argv[0]))
        sys.exist(1)

    data = sys.argv[1]
    run(bytes.fromhex(data), True)

if __name__ == "__main__":
    main()
