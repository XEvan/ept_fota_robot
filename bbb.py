import socket
target_ip = '192.168.0.102'
target_port = 49101
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect((target_ip, target_port))