from abc import ABC, abstractmethod
from mentorhub.models import Goal


class Storage(ABC):
    @abstractmethod
    def save(self, goals: dict[str, Goal]) -> None:
        pass

    @abstractmethod
    def load(self) -> dict[str, Goal]:
        pass


class StorageError(Exception):
    pass


class StorageNotFoundError(StorageError):
    pass


class StorageDecodeError(StorageError):
    pass


class StorageSaveDataError(StorageError):
    pass
