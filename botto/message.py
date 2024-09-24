from dataclasses import dataclass
from enum import Enum


@dataclass
class Message:
    chat_id: int
    date: int
    content: str

    def __eq__(self, other: "Message") -> bool:
        return self.date == other.date

    def __gt__(self, other: "Message") -> bool:
        return self.date > other.date

    def __lt__(self, other: "Message") -> bool:
        return self.date < other.date

    def __ge__(self, other: "Message") -> bool:
        return self.date >= other.date

    def __le__(self, other: "Message") -> bool:
        return self.date <= other.date
