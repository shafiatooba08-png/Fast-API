from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websocket import manager


router = APIRouter()


@router.websocket("/ws/leads/{lead_id}")
async def lead_updates(
    websocket: WebSocket,
    lead_id: int
):

    await manager.connect(
        lead_id,
        websocket
    )

    try:

        while True:

            await websocket.receive_text()


    except WebSocketDisconnect:

        manager.disconnect(
            lead_id,
            websocket
        )