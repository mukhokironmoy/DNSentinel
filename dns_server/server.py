import socket


HOST = "127.0.0.1"
PORT = 2053
BUFFER_SIZE = 512


def main():
    # Create an IPv4 UDP socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Attach the socket to localhost:5353.
    sock.bind((HOST, PORT))

    print(f"DNS UDP server listening on {HOST}:{PORT}")

    while True:
        # Wait for one UDP packet.
        data, address = sock.recvfrom(BUFFER_SIZE)

        # Print sender details.
        print(f"\nReceived {len(data)} bytes from {address}")

        # Print raw packet bytes as hex, not decoded text.
        print(f"Raw hex: {data.hex()}")


if __name__ == "__main__":
    main()