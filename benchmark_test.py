import asyncio
import time
import httpx


BASE_URL = "http://127.0.0.1:8000"


async def send_request(client, endpoint):
    response = await client.get(
        BASE_URL + endpoint
    )
    return response.json()


async def run_benchmark(endpoint):

    async with httpx.AsyncClient(timeout=60) as client:

        tasks = []

        # create 20 concurrent requests
        for _ in range(20):
            tasks.append(
                send_request(
                    client,
                    endpoint
                )
            )

        start_time = time.time()

        await asyncio.gather(*tasks)

        end_time = time.time()

        print(
            endpoint,
            "completed in",
            round(end_time - start_time, 2),
            "seconds"
        )


async def main():

    print("Testing wrong async endpoint...")
    await run_benchmark(
        "/benchmark/wrong"
    )

    print("Testing fixed async endpoint...")
    await run_benchmark(
        "/benchmark/fixed"
    )


asyncio.run(main())