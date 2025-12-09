import sys
import xmlrpc.client
from pathlib import Path

from common import HOST, PORT, list_indexing

client = xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}/")

file = list_indexing(sys.argv, 1) or input("client name pls: ")
name = list_indexing(sys.argv, 2) or input("server name pls: ")

with Path(file).open("rb") as f:
    b = f.read()
r: tuple[str, int] = client.write_file(name, xmlrpc.client.Binary(b))  # type: ignore # im so done
nfn, sz = r
print(f"server wrote file {nfn} with size {sz} bytes")
