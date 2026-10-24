from mentorhub.cli import run_cli
from mentorhub.postrgres_storage import PostgresStorage


def main():
    storage = PostgresStorage()
    run_cli(storage)


if __name__ == "__main__":
    main()
