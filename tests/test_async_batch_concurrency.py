import asyncio
import time
from toon_parse.async_batch_converter import AsyncBatchToonConverter

async def heartbeat():
    """Independent task to verify the event loop is not blocked."""
    beats = 0
    while beats < 10:
        await asyncio.sleep(0.1)
        beats += 1
    return beats

async def verify_concurrency():
    converter = AsyncBatchToonConverter()
    
    # 100 small JSON payloads
    data_list = [{"id": i, "data": "dummy"} for i in range(100)]
    
    print("Starting heartbeat and batch conversion...")
    start_time = time.perf_counter()
    
    # Run heartbeat and conversion concurrently
    heartbeat_task = asyncio.create_task(heartbeat())
    conversion_task = asyncio.create_task(converter.from_json(data_list))
    
    results, beats = await asyncio.gather(conversion_task, heartbeat_task)
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    print(f"Batch completed in {duration:.4f}s")
    print(f"Heartbeat count: {beats} (Should be 10 if not blocked)")
    
    if beats == 10:
        print("✅ SUCCESS: Event loop remained responsive during batch!")
    else:
        print(f"❌ FAILURE: Event loop was blocked! Heartbeat count: {beats}")

    assert len(results) == 100
    assert results[0].startswith("id: 0")

if __name__ == "__main__":
    asyncio.run(verify_concurrency())
