from dataclasses import dataclass

from notice import Notice


@dataclass
class NoticeGroup:
    year: int
    notices: list[Notice]
