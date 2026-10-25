# Test that wait_for() doesn't lose the result of an awaitable that completes
# just after the timeout expires.
# https://github.com/micropython/micropython/issues/19779

try:
    import asyncio
except ImportError:
    print("SKIP")
    raise SystemExit

try:
    import time
except ImportError:
    print("SKIP")
    raise SystemExit


def busy_wait(ms):
    # Block the scheduler so the timeout deadline passes while the awaited
    # task is still running.
    end = time.ticks_add(time.ticks_ms(), ms)
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        pass


async def completes_after_timeout():
    # Let wait_for() start waiting on this task.
    await asyncio.sleep_ms(0)
    # Then complete after the timeout has expired.
    busy_wait(200)
    return 123


async def raises_after_timeout():
    await asyncio.sleep_ms(0)
    busy_wait(200)
    raise ValueError


async def main():
    try:
        print(await asyncio.wait_for(completes_after_timeout(), 0.05))
    except asyncio.TimeoutError:
        print("TimeoutError")

    try:
        await asyncio.wait_for(raises_after_timeout(), 0.05)
    except asyncio.TimeoutError:
        print("TimeoutError")
    except ValueError:
        print("ValueError")


asyncio.run(main())
