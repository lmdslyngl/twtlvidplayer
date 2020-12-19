
import sys
from model import Video, User, Config, TransactionManager


def main():
    with TransactionManager.transaction():
        User.init_table()
        Video.init_table()
        Config.init_table()

    print("Succeeded to init db.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
