import asyncio
import time
import pytest

from api.rate_limiter import AsyncRateLimiter


@pytest.mark.asyncio
async def test_allows_requests_within_limit():
    limiter = AsyncRateLimiter(limit=3, window_seconds=1.0)

    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is True


@pytest.mark.asyncio
async def test_blocks_burst_beyond_limit():
    limiter = AsyncRateLimiter(limit=3, window_seconds=1.0)

    results = []
    for _ in range(5):
        results.append(await limiter.allow("user-1"))

    assert results == [True, True, True, False, False]


@pytest.mark.asyncio
async def test_window_resets_after_expiry():
    limiter = AsyncRateLimiter(limit=2, window_seconds=0.2)

    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is False

    await asyncio.sleep(0.25)

    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is False


@pytest.mark.asyncio
async def test_different_users_are_isolated():
    limiter = AsyncRateLimiter(limit=2, window_seconds=1.0)

    assert await limiter.allow("alice") is True
    assert await limiter.allow("alice") is True
    assert await limiter.allow("alice") is False

    assert await limiter.allow("bob") is True
    assert await limiter.allow("bob") is True
    assert await limiter.allow("bob") is False


@pytest.mark.asyncio
async def test_concurrent_requests_do_not_exceed_limit():
    limiter = AsyncRateLimiter(limit=10, window_seconds=1.0)

    async def make_request():
        return await limiter.allow("user-1")

    results = await asyncio.gather(*[make_request() for _ in range(50)])

    allowed_count = sum(results)
    denied_count = len(results) - allowed_count

    assert allowed_count == 10
    assert denied_count == 40


@pytest.mark.asyncio
async def test_concurrent_requests_no_race_condition_multiple_rounds():
    limiter = AsyncRateLimiter(limit=5, window_seconds=0.3)

    async def burst():
        return await asyncio.gather(
            *[limiter.allow("user-1") for _ in range(20)]
        )

    round1 = await burst()
    assert sum(round1) == 5

    await asyncio.sleep(0.35)

    round2 = await burst()
    assert sum(round2) == 5


@pytest.mark.asyncio
async def test_old_requests_are_pruned_from_window():
    limiter = AsyncRateLimiter(limit=2, window_seconds=0.2)

    assert await limiter.allow("user-1") is True
    await asyncio.sleep(0.11)
    assert await limiter.allow("user-1") is True

    await asyncio.sleep(0.11)

    assert await limiter.allow("user-1") is True
    assert await limiter.allow("user-1") is False


@pytest.mark.asyncio
async def test_does_not_block_event_loop_under_concurrency():
    limiter = AsyncRateLimiter(limit=100, window_seconds=1.0)

    tick_count = 0
    stop = False

    async def ticker():
        nonlocal tick_count
        while not stop:
            tick_count += 1
            await asyncio.sleep(0)

    async def hammer():
        await asyncio.gather(
            *[limiter.allow(f"user-{i % 5}") for i in range(500)]
        )

    ticker_task = asyncio.create_task(ticker())
    start = time.perf_counter()
    await hammer()
    elapsed = time.perf_counter() - start
    stop = True
    await ticker_task

    assert tick_count > 0, "Event loop appears blocked"
    assert elapsed < 2.0, f"Unexpectedly slow: {elapsed:.3f}s"


@pytest.mark.asyncio
async def test_limit_boundary_exactly_n_requests_allowed():
    limiter = AsyncRateLimiter(limit=4, window_seconds=1.0)

    results = [await limiter.allow("user-1") for _ in range(4)]
    assert results == [True, True, True, True]

    assert await limiter.allow("user-1") is False


@pytest.mark.asyncio
async def test_interleaved_users_under_concurrency():
    limiter = AsyncRateLimiter(limit=3, window_seconds=1.0)

    async def make_request(user_id: str):
        return await limiter.allow(user_id)

    tasks = []
    for _ in range(10):
        tasks.append(make_request("alice"))
        tasks.append(make_request("bob"))

    results = await asyncio.gather(*tasks)

    alice_results = results[0::2]
    bob_results = results[1::2]

    assert sum(alice_results) == 3
    assert sum(bob_results) == 3