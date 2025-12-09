import os
import xmlrpc.client
from pathlib import Path
from xmlrpc.server import DocXMLRPCRequestHandler, DocXMLRPCServer

from common import HOST, PORT

with DocXMLRPCServer((HOST, PORT), DocXMLRPCRequestHandler) as server:
    server.register_introspection_functions()

    def write_file(name: str, content: bytes | xmlrpc.client.Binary) -> tuple[str, int]:
        """
        normpath the name and then write content to it

        Args:
            name (str): name of file, could be path. is normpathed.
            content (bytes): content of the file
        Returns:
            (file_name, size) (tuple[str, int]): fuck ts fr

        """
        if isinstance(content, xmlrpc.client.Binary):
            content = content.data
        p = Path(os.path.normpath(name))
        siz = p.write_bytes(content)
        return p.as_posix(), siz

    server.register_function(write_file, "write_file")  # type: ignore # fuck off
    server.serve_forever()
