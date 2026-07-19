import time
import asyncio
from fastapi import APIRouter

router = APIRouter(
    prefix="/benchmark",
    tags=["Benchmark"]
)


@router.get("/wrong")
async def wrong_async_test():

    time.sleep(2)   # ❌ blocking call inside async def

    return {
        "message": "Wrong async endpoint"
    }


@router.get("/fixed")
async def fixed_async_test():

    await asyncio.sleep(2)   # ✅ non-blocking async wait

    return {
        "message": "Fixed async endpoint"
    }