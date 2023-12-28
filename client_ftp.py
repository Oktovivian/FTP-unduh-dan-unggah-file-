import socket
import os


# Fungsi untuk mengirim perintah ke server
def send_command(command, client_socket):
    client_socket.send(command.encode("utf-8"))


# Fungsi untuk mengunduh file dari server
def download_file(filename, client_socket):
    send_command(f"DOWNLOAD {filename}", client_socket)
    data = client_socket.recv(1024)

    if data == b"File not found":
        print(f"File {filename} not found on server.")
        return

    with open(filename, "wb") as file:
        while data:
            try:
                file.write(data)
                client_socket.settimeout(2)  # Set a timeout to break out of the loop
                data = client_socket.recv(1024)
            except socket.timeout:
                break

    print(f"Downloaded {filename} from server.")


# Fungsi untuk mengunggah file ke server
def upload_file(filename, client_socket):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    client_socket.settimeout(5)  # Set timeout to 5 seconds

    send_command(f"UPLOAD {filename}", client_socket)

    try:
        with open(filename, "rb") as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        # Receive confirmation from the server that the file has been fully received
        confirmation = client_socket.recv(1024).decode("utf-8")
        print(confirmation)

    except socket.timeout:
        print("Timeout while waiting for confirmation. Check server status.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"Uploaded {filename} to server.")
    client_socket.settimeout(None)  # Reset timeout to default (blocking)


def connect_toserver():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.143.116", 8888))
    # Set timeout here
    client.settimeout(2)


# Fungsi utama untuk menjalankan klien
def start_client():
    global client
    connect_toserver()
    while True:
        command = input(
            "Enter command (LIST/UPLOAD <filename>/DOWNLOAD <filename>/EXIT): "
        )
        if command.upper() == "EXIT":
            send_command("EXIT", client)
            break
        elif command.upper() == "LIST":
            print("Mengirim perintah LIST")
            send_command("LIST", client)
            print("Menunggu respons dari server")
            data = client.recv(1024).decode("utf-8")
            print("Files on server:\n", data)
        elif command.startswith("UPLOAD"):
            filename = command.split()[1]
            upload_file(filename, client)
            send_command("EXIT", client)
            connect_toserver()
        elif command.startswith("DOWNLOAD"):
            filename = command.split()[1]
            download_file(filename, client)
        else:
            print("Invalid command. Try again.")

    client.close()


if __name__ == "__main__":
    start_client()
