import sys
from pyredis.server.server import server


def main():
    print("Start pyredis")
    server()
    return 0


if __name__ == "__main__":
    sys.exit(main())
