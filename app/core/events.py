from collections import defaultdict

listeners = defaultdict(list)

def register_event(event_name, callback):
    listeners[event_name].append(callback)

def emit_event(event_name, data):
    for callback in listeners[event_name]:
        callback(data)

from app.core.listeners import notify_agent

register_event(
    "lead_status_changed",
    notify_agent
)