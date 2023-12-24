# server.py

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os
from collections import defaultdict
import threading

host = "192.168.183.116"
port = 6969

# Directory tempat file disimpan
UPLOAD_DIR = "uploads"

# Data untuk melacak aktivitas client
client_activity = defaultdict(int)
activity_lock = threading.Lock()


# Fungsi untuk mengunggah file
def upload_file(file_data, file_name):
    with open(os.path.join(UPLOAD_DIR, file_name), "wb") as file:
        file.write(file_data.data)

    # Update aktivitas client

    with activity_lock:
        client_activity[file_data] += 1

    return True


# Fungsi untuk mengunduh file
def download_file(file_name):
    try:
        with open(os.path.join(UPLOAD_DIR, file_name), "rb") as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError:
        return None


# Fungsi untuk mendapatkan aktivitas client
def get_client_activity():
    with activity_lock:
        return dict(client_activity)


# Buat direktori jika belum ada
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Konfigurasi server dengan host dan port yang sudah diinisialisasi
server = SimpleXMLRPCServer((host, port), logRequests=True, allow_none=True)

# Daftarkan fungsi-fungsi RPC
server.register_function(upload_file, "upload_file")
server.register_function(download_file, "download_file")
server.register_function(get_client_activity, "get_client_activity")

print(f"Server listening on {host}:{port}...")
server.serve_forever()
