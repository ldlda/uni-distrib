import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from mpi4py import MPI  # pylint: disable=E0611


comm = MPI.COMM_WORLD
size = comm.Get_size()
assert size >= 2


def list_indexing[T](
    seq: Sequence[T], index: int, default: T | Any | None = None
) -> T | Any | None:
    try:
        return seq[index]
    except IndexError:
        return default


def send_file():
    file = list_indexing(sys.argv, 1) or input("client name pls: ")
    name = list_indexing(sys.argv, 2) or input("server name pls: ")
    name = os.path.normpath(name)
    f = Path(file)
    comm.send((name, f.read_bytes()), dest=1)
    print(f"sent {f.as_posix()} as {name}")


def recv_file():
    name, data = comm.recv(source=0)
    f = Path(os.path.normpath(name))
    sz = f.write_bytes(data)
    print(f"written {f.as_posix()}: {sz} bytes")


rank = comm.Get_rank()
if rank == 0:
    send_file()
else:
    recv_file()
