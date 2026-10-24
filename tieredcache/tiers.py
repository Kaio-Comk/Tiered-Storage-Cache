"""
Two-tier LRU storage manager: Hot Tier (SSD NVMe) + Cold Tier (HDD bulk storage).
"""
from dataclasses import dataclass
from pathlib import Path
import time
import os

@dataclass
class CacheEntry:
    key: str
    path: Path
    size_bytes: int
    last_accessed: float

class CacheTier:
    def __init__(self, name: str, root_dir: Path, max_bytes: int):
        self.name = name
        self.root_dir = root_dir
        self.max_bytes = max_bytes
        self.entries: dict[str, CacheEntry] = {}
        self.current_bytes = 0

    def add(self, key: str, path: Path, size_bytes: int) -> None:
        entry = CacheEntry(key, path, size_bytes, time.time())
        self.entries[key] = entry
        self.current_bytes += size_bytes

    def get(self, key: str) -> Path | None:
        if key in self.entries:
            self.entries[key].last_accessed = time.time()
            return self.entries[key].path
        return None

    def evict_lru(self) -> CacheEntry | None:
        if not self.entries:
            return None
        oldest_key = min(self.entries.keys(), key=lambda k: self.entries[k].last_accessed)
        entry = self.entries.pop(oldest_key)
        self.current_bytes -= entry.size_bytes
        return entry

class TieredCacheManager:
    def __init__(self, hot_tier: CacheTier, cold_tier: CacheTier):
        self.hot = hot_tier
        self.cold = cold_tier

    def lookup(self, key: str) -> Path | None:
        # Check hot SSD first
        if path := self.hot.get(key):
            return path
        # Check cold HDD
        if path := self.cold.get(key):
            return path
        return None

    def store_hot(self, key: str, path: Path, size: int) -> None:
        while (self.hot.current_bytes + size) > self.hot.max_bytes:
            evicted = self.hot.evict_lru()
            if not evicted:
                break
            # Demote to cold tier
            self.cold.add(evicted.key, evicted.path, evicted.size_bytes)
        self.hot.add(key, path, size)
