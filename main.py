import argparse
import socket
import threading


def forward_data(source_client_socket, dest_address, dest_port):
    # 创建一个新的socket连接到目标服务器
    dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dest_socket.connect((dest_address, dest_port))

        # 启动两个线程分别读取和发送数据
        # 一个线程从源客户端读取数据转发给目标服务器
        threading.Thread(target=lambda: _forward(source_client_socket, dest_socket)).start()
        # 另一个线程从目标服务器读取数据转发回源客户端
        threading.Thread(target=lambda: _forward(dest_socket, source_client_socket)).start()

    except Exception as e:
        print(f"Error occurred during forwarding: {e}")
    finally:
        source_client_socket.close()
        dest_socket.close()
        print(f"local port:{local_port}, closed!")


def _forward(src_socket, dest_socket):
    while True:
        data = src_socket.recv(4096)
        if not data:
            break
        dest_socket.sendall(data)


def start_forwarding(local_host, local_port, remote_host, remote_port):
    # 创建监听本地端口的服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_host, local_port))
    server_socket.listen(5)

    print(f"Listening for incoming connections on {local_host}:{local_port}. --> {remote_host}:{remote_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}. Forwarding to {remote_host}:{remote_port}...")
        forward_thread = threading.Thread(target=forward_data, args=(client_socket, remote_host, remote_port))
        forward_thread.start()


if __name__ == "__main__":
    # 设置本地和远程的地址及端口
    local_host = "127.0.0.1"
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('local_port', type=int, help='local TCP port number to listen on', default=8123)
    parser.add_argument('hostname', help='Remote Hostname or IP address to connect to', default=local_host)
    parser.add_argument('port', type=int, help='remote TCP port number to connect to', default=8088)
    args = parser.parse_args()

    local_port = args.local_port
    remote_host = args.hostname
    remote_port = args.port
    try:
        start_forwarding(local_host, local_port, remote_host, remote_port)
    except OSError as e:
        print(e)
    finally:
        print('Closing connection')