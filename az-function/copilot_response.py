# this file is the node.js to python conversion of the https://github.com/copilot-extensions/preview-sdk.js/blob/main/lib/response.js
# as of 2024-10-21

import json

def create_ack_event():
    return create_text_event("")

def create_text_event(message):
    data = {
        "choices": [
            {
                "index": 0,
                "delta": {"content": message, "role": "assistant"},
            },
        ],
    }
    return f"data: {json.dumps(data)}\n\n"

def create_confirmation_event(id, title, message, metadata):
    event = "copilot_confirmation"
    data = {
        "type": "action",
        "title": title,
        "message": message,
        "confirmation": {"id": id, **metadata},
    }
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

def create_references_event(references):
    event = "copilot_references"
    data = references
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

def create_errors_event(errors):
    event = "copilot_errors"
    data = errors
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

def create_done_event():
    data = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "delta": {"content": None},
            },
        ],
    }
    return f"data: {json.dumps(data)}\n\ndata: [DONE]\n\n"