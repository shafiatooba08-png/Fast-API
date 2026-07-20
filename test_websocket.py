import asyncio
import websockets
import requests


LEAD_ID = 124


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc4NDU1NDI0N30.WAcn3Tz7HfziI24fMhc_pduE9RoXIohqlwf2uKOAkmc"


async def test_websocket():

    ws_url = (
        f"ws://localhost:8000/ws/leads/{LEAD_ID}"
    )

    async with websockets.connect(ws_url) as websocket:

        print("WebSocket connected")

        response = requests.patch(
            f"http://localhost:8000/leads/{LEAD_ID}",
            headers={
                "Authorization": f"Bearer {TOKEN}"
            },
            json={
                "status": "qualified"
            }
        )

        print(
            "PATCH response:",
            response.status_code
        )

        message = await websocket.recv()

        print(
            "Received:",
            message
        )


asyncio.run(test_websocket())