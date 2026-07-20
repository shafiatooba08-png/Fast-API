from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections = {}
        self.loop = None


    def set_loop(self, loop):
        self.loop = loop


    async def connect(
        self,
        lead_id: int,
        websocket: WebSocket
    ):
        await websocket.accept()

        if lead_id not in self.active_connections:
            self.active_connections[lead_id] = []

        self.active_connections[lead_id].append(websocket)


    def disconnect(
        self,
        lead_id: int,
        websocket: WebSocket
    ):
        if lead_id in self.active_connections:
            self.active_connections[lead_id].remove(websocket)


    async def send_update(
        self,
        lead_id: int,
        message: dict
    ):

        connections = self.active_connections.get(
            lead_id,
            []
        )

        for websocket in connections:
            await websocket.send_json(message)


manager = ConnectionManager()