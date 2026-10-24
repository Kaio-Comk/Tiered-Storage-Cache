import pytest
import asyncio
from pathlib import Path
from tieredcache import TieredCacheManager, CacheTier, BackpressureController

def test_tier_eviction():
    hot = CacheTier("ssd", Path("/ssd"), max_bytes=100)
    cold = CacheTier("hdd", Path("/hdd"), max_bytes=1000)
    mgr = TieredCacheManager(hot, cold)
    
    mgr.store_hot("video1", Path("/ssd/v1.mp4"), 60)
    mgr.store_hot("video2", Path("/ssd/v2.mp4"), 60)
    
    # video1 was evicted from hot to cold
    assert hot.get("video1") is None
    assert hot.get("video2") is not None
    assert cold.get("video1") is not None

@pytest.mark.asyncio
async def test_backpressure_pause():
    bp = BackpressureController()
    assert not bp.is_throttled
    
    await bp.register_stream_start()
    assert bp.is_throttled
    
    await bp.register_stream_end()
    assert not bp.is_throttled
