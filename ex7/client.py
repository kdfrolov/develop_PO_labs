import socket


def start_client():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = input("Enter message to send: ")
        s.sendall(message.encode("utf-8"))
        data = s.recv(1024)
        print(f"[RECEIVED FROM SERVER] {data.decode('utf-8')}")


if __name__ == "__main__":
    start_client()
