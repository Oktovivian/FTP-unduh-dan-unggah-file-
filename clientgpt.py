import xmlrpc.client
import os


# Fungsi untuk mengunggah file ke server
def upload_file(proxy):
    while True:
        file_path = input(
            "Masukkan path file yang ingin diupload (format: '/path/to/file.ext'): "
        )

        # Memeriksa apakah file dengan path yang dimasukkan ada
        if os.path.exists(file_path):
            break
        else:
            print("File tidak ditemukan. Silakan coba lagi.")

    file_name = input("Masukkan nama file baru (contoh: my_file.txt): ")
    result = proxy.upload(file_path, file_name)
    print(result)


# Fungsi untuk mendownload file dari server
def download_file(proxy):
    files = proxy.list()
    print("Daftar file yang tersedia:")
    for index, file in enumerate(files, start=1):
        print(f"{index}. {file}")

    while True:
        try:
            choice = int(input("Pilih nomor file yang ingin didownload: "))
            if 1 <= choice <= len(files):
                file_name = files[choice - 1]
                content = proxy.download(file_name).data
                with open(file_name, "wb") as file:
                    file.write(content)
                print(f"File '{file_name}' berhasil didownload.")
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan nomor yang sesuai.")
        except ValueError:
            print("Input tidak valid. Masukkan nomor yang sesuai.")


# Fungsi utama untuk menjalankan client
def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        print("\nMenu:")
        print("1. Upload file")
        print("2. Download file")
        print("3. Keluar")
        choice = input("Pilih menu: ")

        if choice == "1":
            upload_file(proxy)
        elif choice == "2":
            download_file(proxy)
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    main()
