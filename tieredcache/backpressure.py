"""
Backpressure controller that automatically pauses background download workers
when active streaming consumers connect, avoiding disk I/O and network saturation.
"""
import asyncio
import time

class BackpressureController:
    def __init__(self, pause_timeout_seconds: float = 30.0):
        self.pause_timeout = pause_timeout_seconds
        self.active_consumers = 0
        self._lock = asyncio.Lock()
        self._event = asyncio.Event()
        self._event.set()

    async def register_stream_start(self) -> None:
        async with self._lock:
            self.active_consumers += 1
            if self.active_consumers == 1:
                self._event.clear()  # Pause background workers

    async def register_stream_end(self) -> None:
        async with self._lock:
            self.active_consumers = max(0, self.active_consumers - 1)
            if self.active_consumers == 0:
                self._event.set()  # Resume background workers

    async def wait_if_throttled(self) -> None:
        """Background workers await this before initiating heavy disk/network writes."""
        await self._event.wait()

    @property
    def is_throttled(self) -> bool:
        return not self._event.is_set()
