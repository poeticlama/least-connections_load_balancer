import argparse
import socket
import threading
import re

IP = '127.0.0.1'
port = 8000
BUFFER = 4096


def handle_request(conn, backend_sockets):
    try:
        # Receiving http request and extract number from it
        http_request = recv_request(conn)

        # Choosing a server using main algorithm
        server_socket = least_connections(backend_sockets)
        with threading.Lock():
            server_socket['connections'] += 1

        # Sending request to this server
        send_request(server_socket, http_request)

        # Handling response
        image_data = recv_response(server_socket)

        # Sending http response to a client
        send_response(image_data, conn)

    except Exception as e:
        print(f"Error in request handling: {str(e)}")
        error_response = (
            b"HTTP/1.1 500 Internal Server Error\r\n"
            b"Content-Type: text/plain\r\n\r\n"
            b"Server Error"
        )
        conn.sendall(error_response)

    finally:
        if server_socket:
            with threading.Lock():
                server_socket['connections'] -= 1
        conn.close()


def recv_request(conn):
    http_request = b""
    while True:
        data = conn.recv(BUFFER)
        if not data:  # Connection closed
            break
        http_request += data

    # Returning a http request we got from a client
    return http_request


def least_connections(backend_sockets):
    servers = sorted(backend_sockets, key=lambda x: x['connections'])
    return servers[0]


def send_request(server_socket, http_request):
    # Sending a request we got from a client to chosen server
    try:
        request_text = http_request.decode("utf-8")
    except UnicodeDecodeError:
        return None
    request = re.sub(r'Host: (\d+\.){3}\d+:\d+', f'Host: {server_socket['address']}', request_text)
    server_socket['socket'].sendall(request.encode('utf-8'))


def recv_response(server_socket):
    # Receiving a response from a server
    response = b''
    while True:
        chunk = server_socket['socket'].recv(BUFFER)
        if not chunk:
            break
        response += chunk
    header_end = response.find(b"\r\n\r\n")
    image_data = response[header_end + 4:]

    return image_data


def send_response(image_data, conn):
    if not image_data:
        response = (
            b"HTTP/1.1 500 Internal Server Error\r\n"
            b"Content-Type: text/plain\r\n\r\n"
            b"Error loading image"
        )
    else:
        response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Connection: close\r\n\r\n" +
                image_data
        )

    conn.sendall(response)


def parse_args():
    # Taking addresses (with ports) of backend servers when starting a balancer
    parser = argparse.ArgumentParser()
    parser.add_argument('back_addresses', nargs='+', type=str)

    args = parser.parse_args()
    back_addresses = args.back_addresses

    # Return a list of these addresses
    return back_addresses


def create_sockets():
    # Creating sockets from addresses we got
    addresses = parse_args()
    sockets = []

    for addr in addresses:
        server_ip, server_port = addr.split(":")
        server_port = int(server_port)

        # Creating a socket for corresponding backend address
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.connect((server_ip, server_port))

        # Appending to the list of sockets
        sockets.append({
            'socket': new_socket,
            'connections': 0,
            'address': f'{server_ip}:{server_port}'
        })

    return sockets


def main():
    backend_sockets = create_sockets()

    # Connect to frontend app
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Some configuration for socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, port))
        sock.listen()

        try:
            while True:
                # Accepting a new connection from client
                conn, addr = sock.accept()

                # Implementing multithreading for different responses
                thread = threading.Thread(
                    target=handle_request,
                    args=(conn, addr, backend_sockets)
                )
                thread.start()
        except:
            print("Error")
        finally:
            sock.close()


if __name__ == '__main__':
    main()