from typing import Dict

def suspicious_message_creator(message_type: int, message) -> Dict:
    """if message_type == 1 then the message_type is suspicious 
    else if message_type == 2 then message_type is very suspicious
    """

    if message_type == 1:
        return {"type": "suspicious", "description": message}
    elif message_type == 2:
        return {"type": "very suspicious", "description": message}
    else:
        raise("Unknown message type")
