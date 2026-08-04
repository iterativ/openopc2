from queue import Empty, Queue
from typing import Iterator, Optional

try:
    import Pyro5.api
except ImportError:
    class _PyroApi:
        @staticmethod
        def expose(cls):
            return cls

    class _Pyro5:
        api = _PyroApi()

    Pyro5 = _Pyro5()

from openopc2.ae_types import AeEventBatch, AeFilter


@Pyro5.api.expose
class OpcAeSubscription:
    def __init__(
        self,
        subscription_backend=None,
        filter: AeFilter | None = None,
        returned_attributes: dict[int, list[int]] | None = None,
        queue: Queue | None = None,
    ):
        self._backend = subscription_backend
        self.filter = filter or AeFilter()
        self.returned_attributes = returned_attributes or {}
        self._queue = queue or Queue()
        self.closed = False

    def enqueue_batch(self, batch: AeEventBatch):
        self._queue.put(batch)

    def next_batch(self, timeout: Optional[float] = None) -> AeEventBatch | None:
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            return None

    def batches(self, timeout: Optional[float] = None) -> Iterator[AeEventBatch]:
        while not self.closed:
            batch = self.next_batch(timeout=timeout)
            if batch is None:
                break
            yield batch

    def events(self, timeout: Optional[float] = None):
        for batch in self.batches(timeout=timeout):
            for event in batch.events:
                yield event

    def refresh(self):
        if self._backend is not None:
            return self._backend.refresh()
        return None

    def get_state(self):
        if self._backend is not None:
            return self._backend.get_state()
        return None

    def close(self):
        self.closed = True
        if self._backend is not None:
            close = getattr(self._backend, "close", None)
            if close is not None:
                close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()
