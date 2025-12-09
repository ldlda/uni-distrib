import base64
import io
import os
import select
import socket
from pathlib import Path

from common import (
    FILE_NAME,
    FILE_SIZE,
    HOST,
    PORT,
    SEP,
    Ahhdress,
    Host,
    Port,
    setup_debug_handlers,
)

setup_debug_handlers()


def server_init(host: Host, port: Port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    return server


def accept_request(server: socket.socket) -> tuple[Ahhdress, str | None, bytes | None]:
    conn, addr = server.accept()
    try:
        things = conn.makefile("rwb")
        try:
            fn, content = eat(things)
        except ValueError as e:
            print(f"Error from {addr}: {e}")
            return addr, None, None
        things.write(FILE_NAME + base64.standard_b64encode(fn.encode()) + SEP)
        things.write(FILE_SIZE + (b"%d" % len(content)) + SEP + SEP)
        things.flush()
        return addr, fn, content
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
        print(f"Connection error with {addr}: {e}")
        return addr, None, None
    finally:
        conn.close()


def eat(things: io.BufferedRWPair) -> tuple[str, bytes]:
    fn = things.readline()
    if fn.startswith(FILE_NAME):
        file_name = base64.standard_b64decode(
            fn.removeprefix(FILE_NAME).removesuffix(SEP)
        ).decode()
    else:
        raise ValueError("no file name")
    fz = things.readline()
    if fz.startswith(FILE_SIZE):
        file_size = int(fz.removeprefix(FILE_SIZE).removesuffix(SEP))
    else:
        raise ValueError("no file size")
    if not SEP == things.readline():
        raise ValueError("schema violated")
    file = things.read(file_size)
    if len(file) != file_size:
        raise ValueError("file size different")
    if things.read(2) != SEP + SEP:
        raise ValueError("schema violated")
    return file_name, file


server = server_init(HOST, PORT)
print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        readable, _, _ = select.select([server], [], [], 1.0)
        if server in readable:
            addr, file_name, file_content = accept_request(server)

            if file_name is None or file_content is None:
                continue

            file_new = os.path.normpath(file_name)
            print(f"file {file_name} i meant {file_new} is Being Made")
            Path(file_new).write_bytes(file_content)
except KeyboardInterrupt:
    print("\nServer stopping...")
finally:
    server.close()
