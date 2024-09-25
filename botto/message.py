from dataclasses import dataclass
from enum import Enum


@dataclass
class Message:
    chat_id: int
    update_id: int
    content: str

    def __eq__(self, other: "Message") -> bool:
        return self.update_id == other.update_id

    def __gt__(self, other: "Message") -> bool:
        return self.update_id > other.update_id

    def __lt__(self, other: "Message") -> bool:
        return self.update_id < other.update_id

    def __ge__(self, other: "Message") -> bool:
        return self.update_id >= other.update_id

    def __le__(self, other: "Message") -> bool:
        return self.update_id <= other.update_id
