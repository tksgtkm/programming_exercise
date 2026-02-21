import os
import asyncio
import json
import typing as T

FileWithId = T.Tuple[str, str]
Occurrences = T.Dict[str, str]

PORT = 12345
HOST = "127.0.0.1"
TEMP_DIR = "temp"
END_MSG = b"EOF"

class Protocol(asyncio.Protocol):

    def __init__(self) -> None:
        super().__init__()
        self.buffer = b""
    
    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport
        print("Connection made")
    
    def data_received(self, data: bytes) -> None:
        self.buffer += data
        if END_MSG in self.buffer:
            if b":" not in data:
                command, _ = self.buffer.split(END_MSG, 1)
                data = None
            else:
                command, data = self.buffer.split(b":", 1)
                data, self.buffer = data.split(END_MSG, 1)
                data = json.loads(data.decode())
            self.process_command(command, data)
    
    def send_command(self, command, data: FileWithId = None) -> None:
        if data:
            pdata = json.dumps(data).encode()
            self.transport.write(command + b":" + pdata + END_MSG)
        else:
            self.transport.write(command + END_MSG)

    def get_temp_dir(self) -> str:
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)
    
    def process_command(self, command: bytes, data):
        raise NotImplementedError