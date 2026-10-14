from mentorhub.cli import run_cli
from mentorhub.storage import InMemoryStorage, JsonStorage

storage = JsonStorage('data.json')

test_storage = InMemoryStorage()

run_cli(storage)
