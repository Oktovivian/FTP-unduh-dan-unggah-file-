from xmlrpc.server import SimpleXMLRPCServer
import os
import xmlrpc.client

# Inisialisasi daftar file yang tersedia di server
available_files = []


# Fungsi untuk mengunggah file ke server
def upload_file(file_path, file_name):
    try:
        with open(file_path, "rb") as file:
            content = file.read()
            with open(file_name, "wb") as new_file:
                new_file.write(content)
                available_files.append(file_name)
            return f"File '{file_name}' berhasil diupload."
    except FileNotFoundError:
        return "File tidak ditemukan."


# Fungsi untuk men-download file dari server
def download_file(file_name):
    if file_name in available_files:
        try:
            with open(file_name, "rb") as file:
                content = file.read()
                return xmlrpc.client.Binary(content)
        except FileNotFoundError:
            return "File tidak ditemukan."
    else:
        return "File tidak tersedia untuk di-download."


# Fungsi untuk menampilkan daftar file yang tersedia di server
def list_files():
    return available_files


# Inisialisasi server RPC
server = SimpleXMLRPCServer(("localhost", 8000))
print("Server berjalan di port 8000...")

# Register fungsi-fungsi ke server
server.register_function(upload_file, "upload")
server.register_function(download_file, "download")
server.register_function(list_files, "list")

# Jalankan server secara terus menerus
server.serve_forever()
