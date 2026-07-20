from collections import defaultdict

from app.core.listeners import notify_agent
from app.core.websocket_listener import notify_websocket


listeners = defaultdict(list)


def register_event(event_name, callback):
    listeners[event_name].append(callback)


def emit_event(event_name, data):
    for callback in listeners[event_name]:
        callback(data)


# Existing listener
register_event(
    "lead_status_changed",
    notify_agent
)


# WebSocket listener
register_event(
    "lead_status_changed",
    notify_websocket
)