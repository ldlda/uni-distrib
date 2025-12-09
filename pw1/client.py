import base64
import os
import socket
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from common import FILE_NAME, FILE_SIZE, HOST, PORT, SEP, setup_debug_handlers

setup_debug_handlers()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def send(client: socket.socket, file: Path, name: str | None) -> tuple[str, int]:
    if name is None:
        name = os.path.normpath(file.relative_to(Path.cwd()))
    client.send(FILE_NAME + base64.standard_b64encode(name.encode()) + SEP)
    fz = os.path.getsize(file)
    client.send(FILE_SIZE + str(fz).encode() + SEP + SEP)
    with file.open("rb") as f:
        client.sendfile(f)
    client.send(SEP + SEP)
    return name, fz


def shit(client: socket.socket, file: Path) -> tuple[str, int]:
    thing = client.makefile("rb")
    a = thing.readline()
    if a.startswith(FILE_NAME):
        fn = base64.standard_b64decode(
            a.removeprefix(FILE_NAME).removesuffix(SEP)
        ).decode()
    else:
        raise ValueError("schema violated")
    a = thing.readline()
    if a.startswith(FILE_SIZE):
        fz = int((a.removeprefix(FILE_SIZE).removesuffix(SEP)).decode())
    else:
        raise ValueError("schema violated")
    if thing.readline() != SEP:
        raise ValueError("schema violated")
    return fn, fz


def list_indexing[T](
    seq: Sequence[T], index: int, default: T | Any | None = None
) -> T | Any | None:
    try:
        return seq[index]
    except IndexError:
        return default


fn = Path(list_indexing(sys.argv, 1) or input("file name pls: "))
if fn.is_file():
    n = list_indexing(sys.argv, 2) or input("name of sent file pls: ")
    print(f"file {fn} as {n} sending")
    nn, fz = send(client, fn, n if n else None)
    rn, rfz = shit(client, fn)
    print(f"new file {nn} sent with {fz} bytes, received {rfz} bytes as {rn}")
else:
    print(f"wtf is {fn}")

client.close()
