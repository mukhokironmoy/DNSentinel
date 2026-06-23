import struct

def parse_header(data: bytes) -> dict:
    """
    Parse the fixed 12 byte DNS header from a raw DNS packet
    """

    if len(data)<12:
        raise ValueError("DNS packet too short to contain a valid header")
    
    # Fetch the first 12 fields to construct the header
    fields = struct.unpack('!HHHHHH', data[:12])

    return {
        'transaction_id' : fields[0],
        'flags' : fields[1],
        'qdcount' : fields[2],
        'ancount' : fields[3],
        'nscount' : fields[4],
        'arcount' : fields[5],
    }


def pack_header(header: dict) -> bytes:
    """
    Pack a DNS header dictionary back into the fixed length 12 byte DNS header format.
    """

    return struct.pack(
        '!HHHHHH',
        header['transaction_id'],
        header['flags'],
        header['qdcount'],
        header['ancount'],
        header['nscount'],
        header['arcount'],
    )