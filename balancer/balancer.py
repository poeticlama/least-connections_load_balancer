import argparse
import socket
import os
import threading

IP = '127.0.0.1'
port = 8000
# PATH = '/images/2'

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'received_image.jpg')


def handle_request():
    # Some pseudocode below to illustrate main idea
    accept_client() # Accepting a new connection
    recv_request() # Receiving http request
    least_connections() # Choosing a server using main algorithm
    send_request() # Sending request to this server
    recv_response() # Handling response
    send_response() # Sending http response to a client
    pass


def accept_client():
    # Here is what we should do when we got a new connection from a client.
    pass


def recv_request():
    # Some logic for working with a client request
    pass


def least_connections():
    # Here is the place for main algorithm
    pass


def send_request():
    # Sending a request we got from a client to chosen server
    pass


def recv_response():
    # Receiving a response from a server
    pass


def send_response():
    # Sending a response to a client
    pass


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
        sockets.append(new_socket)

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
                    args=(conn, addr)
                )
                thread.start()

                # # Some code to be placed in on_accept() function
                # # Variable "num" is just an index of picture that we got from client
                #
                # num = 2
                # request = \
                #     f'GET /images/{num} HTTP/1.1\r\n'\
                #     f'Host: {IP}:{port}\r\n'\
                #     'Connection: close\r\n'\
                #     '\r\n'
                # sock.sendall(request.encode('utf-8'))
                # response = b''
                # while True:
                #     chunk = sock.recv(1024)
                #     if not chunk:
                #         break
                #     response += chunk
                # header_end = response.find(b"\r\n\r\n")
                # headers = response[:header_end].decode()
                # image_data = response[header_end+4:]
                #
                # with open(path, "wb") as f:
                #     f.write(image_data)

        except:
            print("Error")
        finally:
            sock.close()
