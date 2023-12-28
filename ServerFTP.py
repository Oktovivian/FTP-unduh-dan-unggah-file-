import socket
import threading
import os
import time

# Global variable untuk melacak aktivitas klien
client_activity = {}


# Fungsi untuk menangani setiap koneksi klien
def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")

    # Menambah nilai aktivitas jika alamat sudah ada di kamus, jika belum set ke 0
    client_activity[address] = client_activity.get(address, 0)

    try:
        while True:
            # Menerima perintah dari klien
            command = client_socket.recv(1024).decode("utf-8")

            if not command:
                break  # Keluar dari loop jika tidak ada perintah yang diterima

            # Menambah nilai aktivitas hanya untuk perintah 'DOWNLOAD' dan 'UPLOAD'
            if command.startswith("DOWNLOAD") or command.startswith("UPLOAD"):
                client_activity[address] += 1

            if command == "LIST":
                # Mengirim daftar file ke klien
                files = os.listdir(".")
                file_list = "\n".join(files)
                client_socket.send(file_list.encode("utf-8"))

            elif command.startswith("DOWNLOAD"):
                # Ekstrak nama file dari perintah
                filename = command.split()[1]

                try:
                    # Membuka dan mengirim file ke klien
                    with open(filename, "rb") as file:
                        data = file.read(1024)
                        while data:
                            client_socket.send(data)
                            data = file.read(1024)

                    # Menambahkan jeda kecil untuk memungkinkan klien memproses akhir file
                    time.sleep(0.1)

                except FileNotFoundError:
                    # Mengirim pesan kesalahan jika file tidak ditemukan
                    client_socket.send("File not found".encode("utf-8"))

            elif command.startswith("UPLOAD"):
                # Menerima nama file dari klien
                filename = command.split()[1]

                # Menerima dan menulis data file
                with open(filename, "wb") as file:
                    data = client_socket.recv(1024)
                    while data:
                        file.write(data)
                        data = client_socket.recv(1024)

                # Mengirim konfirmasi ke klien bahwa file telah diterima dengan sukses
                client_socket.send("File uploaded successfully".encode("utf-8"))
                print(f"Received {filename} from {address}")

            elif command == "EXIT":
                print(f"Closing connection with {address}")
                break

    except ConnectionAbortedError:
        print(f"Connection with {address} aborted.")

    finally:
        # Menutup soket klien
        client_socket.close()


# Fungsi untuk menampilkan klien paling aktif
def display_most_active_client():
    while True:
        # Menampilkan klien paling aktif setiap 10 detik
        time.sleep(10)

        # Memeriksa apakah kamus client_activity tidak kosong
        if client_activity:
            most_active_client_address = max(client_activity, key=client_activity.get)
            most_active_client_count = client_activity[most_active_client_address]
            print(
                f"Most active client: {most_active_client_address} with activity count: {most_active_client_count}"
            )
        else:
            print("No active clients.")


# Fungsi untuk memulai server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.60.226.85", 8888))
    server.listen(5)

    print("Server listening on port 8888")

    # Memulai thread display_most_active_client
    threading.Thread(target=display_most_active_client, daemon=True).start()

    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()


if __name__ == "__main__":
    start_server()
