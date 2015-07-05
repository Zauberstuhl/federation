import importlib

from federation.exceptions import NoSuitableProtocolFoundError


PROTOCOLS = (
    "diaspora",
)


def handle_receive(payload, user=None, sender_key_fetcher=None):
    """Takes a payload and passes it to the correct protocol.

    Args:
        payload (str)                           - Payload blob
        user (optional, obj)                    - User that will be passed to `protocol.receive`
        sender_key_fetcher (optional, func)     - Function that accepts sender handle and returns public key
    """
    found_protocol = None
    for protocol_name in PROTOCOLS:
        protocol = importlib.import_module("federation.protocols.%s.protocol" % protocol_name)
        if protocol.identify_payload(payload):
            found_protocol = protocol
            break

    if found_protocol:
        protocol = found_protocol.Protocol()
        sender, message = protocol.receive(payload, user, sender_key_fetcher)
    else:
        raise NoSuitableProtocolFoundError()

    mappers = importlib.import_module("federation.entities.%s.mappers" % found_protocol.PROTOCOL_NAME)
    entities = mappers.message_to_objects(message)

    return sender, found_protocol.PROTOCOL_NAME, entities


def handle_send():
    """Send."""
    pass
