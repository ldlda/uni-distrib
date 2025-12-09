from collections.abc import Sequence
from typing import Any, Protocol, overload, override

HOST = "127.0.0.1"
PORT = 9870


class Lda(Protocol):
    def write_file(self, name: str, content: bytes): ...


# no this means no typechecking unfortunately
@overload
def list_indexing[T](seq: Sequence[T], index: int, default: T) -> T: ...


@overload
def list_indexing[T](
    seq: Sequence[T], index: int, default: T | None = None
) -> T | None: ...


@overload
def list_indexing[T](
    seq: Sequence[T], index: int, default: T | Any | None = None
) -> T | Any | None: ...


def list_indexing(seq: Sequence, index: int, default: Any | None = None) -> Any | None:
    try:
        return seq[index]
    except IndexError:
        return default
