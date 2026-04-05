import asyncio
import time
from collections import defaultdict


class AsyncRateLimiter:
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        # BUG: no lock, so concurrent requests can race

    async def allow(self, user_id: str) -> bool:
        now = time.time()

        # BUG 1:
        # Checks limit before pruning expired timestamps.
        # This can incorrectly deny requests even after the window should reset.
        if len(self.requests[user_id]) >= self.limit:
            return False

        # BUG 2:
        # Expired timestamps are pruned too late.
        self.requests[user_id] = [
            ts for ts in self.requests[user_id]
            if now - ts < self.window_seconds
        ]

        # BUG 3:
        # No synchronization, so concurrent requests can overshoot the limit.
        await asyncio.sleep(0)

        self.requests[user_id].append(now)
        return True