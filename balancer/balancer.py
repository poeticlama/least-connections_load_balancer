import argparse
import socket
import os
import threading
import re

IP = '127.0.0.1'
port = 8000
BUFFER = 4096
# PATH = '/images/2'

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'received_image.jpg')


def handle_request(conn, address, backend_sockets):
    # Some pseudocode below to illustrate main idea

    # Receiving http request and extract number from it
    http_request = recv_request(conn, address)

    # num = extract_image_number(http_request)

    # Choosing a server using main algorithm
    server_socket = least_connections(backend_sockets)

    # Sending request to this server
    # send_request(server_socket, num)
    send_request(server_socket, http_request)

    # Handling response
    image_data = recv_response(server_socket)

    # Sending http response to a client
    send_response(image_data, conn)


def recv_request(conn, address):
    # Some logic for working with a client request

    # Receiving from client until finish
    http_request = b""
    while True:
        data = conn.recv(BUFFER)
        if not data:    # Connection closed
            break
        http_request += data

    # Returning a http request we got from a client
    return http_request


# def extract_image_number(http_request: bytes):
#     try:
#         request_text = http_request.decode("utf-8")
#     except UnicodeDecodeError:
#         return None

#     headers_part, _, _ = request_text.partition("\r\n\r\n")
#     headers_lines = headers_part.split("\r\n")

#     for header in headers_lines[1:]:
#         if header.startswith("Image Number:"):
#             _, value = header.split(":", 1)
#             image_num_str = value.strip()
#             try:
#                 return int(image_num_str)
#             except ValueError:
#                 return None

#     return None


def least_connections(backend_sockets):
    # Here is the place for main algorithm and after its execution
    # it returns backend_socket chosen
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
    headers = response[:header_end].decode()
    image_data = response[header_end + 4:]

    # TODO: check if image_data is enough to send http response with an image

    # Returning image_data (just because I have no idea what we should
    # send in http response)

    # with open(path, "wb") as f:
    #     f.write(image_data)
    return image_data


def send_response(image_data, conn):
    # Sending a response to a client
    # Here we should somehow create a new http response with image_data
    # TODO: create a response with an image we got
    if not response:
        # Add failures
        response = (
            b"HTTP/1.1 500 Internal Server Error\r\n"
            b"Content-Type: text/plain\r\n\r\n"
            b"Error loading image"
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
        # sockets.append(new_socket)
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
