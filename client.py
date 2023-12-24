import xmlrpc.client
import base64


# Fungsi untuk membaca file sebagai byte array
def read_file(file_path):
    with open(file_path, "rb") as file:
        return xmlrpc.client.Binary(file.read())


# Ganti host dan port sesuai dengan konfigurasi server.py
host = "192.168.1.30"  # Ganti dengan alamat IP atau hostname server
port = 6969  # Ganti dengan port yang digunakan oleh server

# Konfigurasi server
server = xmlrpc.client.ServerProxy(f"http://{host}:{port}")


# Fungsi untuk mengunggah file
def upload_file(file_path):
    file_name = file_path.split("/")[-1]
    file_data = read_file(file_path)

    # Simpan file di server
    result = server.upload_file(file_data, file_name)
    if result:
        print(f"File '{file_name}' berhasil diunggah.")
    else:
        print(f"File '{file_name}' gagal diunggah.")


# Fungsi untuk mengunduh file
def download_file(file_name):
    file_data = server.download_file(file_name)

    if file_data is not None:
        with open(file_name, "wb") as file:
            file.write(base64.b64decode(file_data))
        print(f"File '{file_name}' berhasil diunduh.")
    else:
        print(f"File '{file_name}' tidak ditemukan di server.")


# Fungsi untuk mendapatkan aktivitas client
def get_client_activity():
    client_activity = server.get_client_activity()
    if client_activity:
        print("Aktivitas client:")
        for client_id, count in client_activity.items():
            print(f"Client {client_id}: {count} file")
    else:
        print("Tidak ada aktivitas client.")


# Contoh penggunaan
upload_file("file_to_upload.txt")
# upload_file("file.txt")
# download_file("example.jpg")
# get_client_activity()
