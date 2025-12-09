import atexit
import signal
import sys
import traceback
from typing import Any, Sequence

type Host = str
type Port = int
type Ahhdress = tuple[Host, Port]

HOST = "127.0.0.1"
PORT = 9870

FILE_NAME = b"FILE: "
FILE_SIZE = b"SIZE: "
SEP = b"\n"

# schema:
# client: FILE file name b64 SEP SIZE no of bytes SEP SEP file content SEP SEP
# server: FILE file name b64 SEP SIZE no of bytes SEP SEP
# http ahhhhhhhhhhhhh


def dump_trace(signum, frame):
    print(f"\nSignal {signum} received. Stack trace:")
    traceback.print_stack(frame)
    sys.exit(1)


def setup_debug_handlers():
    atexit.register(lambda: print("Program exiting."))
    signal.signal(signal.SIGTERM, dump_trace)
    signal.signal(signal.SIGINT, dump_trace)


def list_indexing[T](
    seq: Sequence[T], index: int, default: T | Any | None = None
) -> T | Any | None:
    try:
        return seq[index]
    except IndexError:
        return default
