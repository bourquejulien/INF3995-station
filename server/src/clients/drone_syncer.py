from threading import Event, Lock

DEFAULT_TIMEOUT_SEC = 5


class DroneSyncer:
    _uris: list[str]
    _blocked_uris: list[str]
    _mutex: Lock
    _event: Event

    def __init__(self, uris: list[str]):
        self._uris = uris
        self._blocked_uris = []
        self._mutex = Lock()
        self._event = Event()

        self._event.set()

    def wait(self, timeout: int = DEFAULT_TIMEOUT_SEC):
        with self._mutex:
            if self._event.is_set():
                self._event.clear()
                self._blocked_uris = self._uris

        return self._event.wait(timeout)

    def release(self, uri: str):
        if self._event.is_set():
            return

        with self._mutex:
            if uri in self._blocked_uris:
                self._blocked_uris.remove(uri)
            if len(self._blocked_uris) == 0:
                self._event.set()

    def remove_uri(self, uri):
        self._uris.remove(uri)
        self.release(uri)

    def close(self):
        with self._mutex:
            self._uris = []
            self._blocked_uris = []
            self._event.set()
