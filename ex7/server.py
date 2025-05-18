import socket
import threading


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            print(f"[RECEIVED] {data}")
            response = f"Server received: {data}"
            conn.send(response.encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[CONNECTION CLOSED] {addr} disconnected.")


def start_server():
    HOST = "127.0.0.1"  # Стандартный loopback interface address (localhost)
    PORT = 65432  # Порт

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    start_server()
