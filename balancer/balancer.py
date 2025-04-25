import socket
import os

IP = '127.0.0.1'
port = 8000
PATH = '/images/2'

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'received_image.jpg')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((IP, port))
        request = \
            f'GET {PATH} HTTP/1.1\r\n'\
            f'Host: {IP}:{port}\r\n'\
            'Connection: close\r\n'\
            '\r\n'
        sock.sendall(request.encode('utf-8'))
        response = b''
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk
        header_end = response.find(b"\r\n\r\n")
        headers = response[:header_end].decode()
        image_data = response[header_end+4:]
        
        with open(path, "wb") as f:
            f.write(image_data)
    except:
        print("Error")
    finally:
        sock.close()
