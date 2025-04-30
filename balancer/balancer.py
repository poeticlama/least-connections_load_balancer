import argparse
import socket
import threading
import re
from traffic_visualizer import plot_traffic

IP = '127.0.0.1'
port = 8000
BUFFER = 4096


def handle_request(conn, backend_addresses, connection_counts):
    backend_addr = None
    try:
        # Receiving http request from client
        print("Handling request from socket: ", conn)
        http_request = recv_request(conn)

        with threading.Lock():
            # Choosing a server using algorithm
            backend_addr = least_connections(backend_addresses, connection_counts)
            connection_counts[backend_addr] += 1

        # Sending request to this server
        response = forward_to_backend(backend_addr, http_request)

        # Sending response
        conn.sendall(response)

    except Exception as e:
        print(f"Error in request handling: {str(e)}")
        error_response = (
            b"HTTP/1.1 500 Internal Server Error\r\n"
            b"Content-Type: text/plain\r\n\r\n"
            b"Server Error"
        )
        conn.sendall(error_response)

    finally:
        if backend_addr:
            with threading.Lock():
                connection_counts[backend_addr] -= 1
        conn.close()


def recv_request(conn):
    http_request = b""
    data = conn.recv(BUFFER)
    http_request += data

    # Returning a http request we got from a client
    return http_request


def least_connections(backend_addresses, connection_counts):
    return sorted(backend_addresses, key=lambda addr: connection_counts[addr])[0]


def forward_to_backend(backend_addr, http_request):
    host, back_port = backend_addr.split(':')
    back_port = int(back_port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_sock:
        backend_sock.connect((host, back_port))

        # Sending a request to backend
        request_text = http_request.decode("utf-8", errors='ignore')
        request_text = re.sub(r'Host: (\d+\.){3}\d+:\d+', f'Host: {backend_addr}', request_text)
        backend_sock.sendall(request_text.encode("utf-8"))

        # Getting a response
        response = b''
        while True:
            chunk = backend_sock.recv(BUFFER)
            if not chunk:
                break
            response += chunk

        return response


def parse_args():
    # Taking addresses (with ports) of backend servers when starting a balancer
    parser = argparse.ArgumentParser()
    parser.add_argument('back_addresses', nargs='+', type=str)

    args = parser.parse_args()
    back_addresses = args.back_addresses

    # Return a list of these addresses
    return back_addresses


def main():
    backend_addresses = parse_args()
    connection_counts = {addr: 0 for addr in backend_addresses}

    # Connect to frontend app
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Some configuration for socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, port))
        sock.listen()

        try:
            # plot_traffic(connection_counts)
            plot_thread = threading.Thread(target=plot_traffic, args=[connection_counts])
            plot_thread.start()
            while True:
                # Accepting a new connection from client
                conn, addr = sock.accept()
                print("Got new connection from client: ", addr[1])

                # Implementing multithreading for different responses
                thread = threading.Thread(
                    target=handle_request,
                    args=(conn, backend_addresses, connection_counts)
                )
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            sock.close()


if __name__ == '__main__':
    main()
