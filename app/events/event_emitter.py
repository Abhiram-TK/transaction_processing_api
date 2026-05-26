from datetime import datetime

def emit_event(event_name: str, payload: dict):

    timestamp = datetime.utcnow()

    event_message = (f"\nEVENT EMITTED\n" f"\nTime: {timestamp}\n" f"Event: {event_name}\n" f"Payload: {payload}\n")

    print(event_message)

    with open("events.log", "a") as log_file:

        log_file.write(event_message)

