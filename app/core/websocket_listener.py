import asyncio

from app.core.websocket import manager


def notify_websocket(lead):

    message = {
        "event": "lead_status_changed",
        "lead_id": lead.id,
        "status": lead.status
    }

    if manager.loop:

        asyncio.run_coroutine_threadsafe(
            manager.send_update(
                lead.id,
                message
            ),
            manager.loop
        )