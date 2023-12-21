import os

from dotenv import load_dotenv


def main():
    load_dotenv()


if __name__ == "__main__":
    main()
    AOC_SESSION = os.environ["AOC_SESSION"]
