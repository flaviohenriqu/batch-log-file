from logging import Handler

from immudb import ImmudbClient


class ImmudbHandler(Handler):
    def __init__(self, url: str, port: str, user: str = "immudb", password: str = "immudb"):
        Handler.__init__(self)
        self.immudb_client = ImmudbClient(f"{url}:{port}")
        self.immudb_client.login(user, password)
        try:
            self.immudb_client.useDatabase("logging")
        except Exception:
            self.immudb_client.createDatabase("logging")
            self.immudb_client.useDatabase("logging")

    def emit(self, record):
        payload = self.format(record)
        self.immudb_client.set(b"INFO", bytes(payload.encode("utf-8")))
