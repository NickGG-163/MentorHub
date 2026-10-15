from mentorhub.cli import run_cli
from mentorhub.storage import JsonStorage


def main():
    storage = JsonStorage("data.json")
    run_cli(storage)


if __name__ == "__main__":
    main()
