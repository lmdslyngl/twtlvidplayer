
import sys
from model import Video, Config, TransactionManager


def main():
    with TransactionManager.transaction():
        Video.init_table()
        Config.init_table()

    print("Succeeded to init db.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
