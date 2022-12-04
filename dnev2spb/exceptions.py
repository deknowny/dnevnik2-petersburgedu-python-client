import dataclasses


@dataclasses.dataclass
class BadRequestError(Exception):
    status: int
