import socket
from des import encrypt, string_to_int, int_to_string

kunci = 0xABCDEF1234567890

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # membuat objek socket, AF-INET : protokol IPv4, SOCK_STREAM : socket tipe stream untuk TCP
server_address = ('localhost', 10235)
client_socket.connect(server_address)
print("Terhubung ke server di", server_address)

while True:
    # Meminta pengguna memasukkan pesan untuk dikirim ke server
    message_to_send = input("--> Client: ")
    
    # Jika client mengetik "exit123", client menutup koneksi
    if message_to_send.lower() == "exit123":
        print("Anda meminta penutupan koneksi.")
        message_to_send = "koneksi ditutup oleh client"
        # encrypted_message = encrypt(string_to_int(message_to_send), kunci)
        client_socket.sendall(str(message_to_send).encode('utf-8'))
        break  # Koneksi ditutup oleh client

    # Mengirim pesan terenkripsi ke server
    encrypted_message = encrypt(string_to_int(message_to_send), kunci)
    print("Pesan terenkripsi yang dikirim: ", encrypted_message)
    client_socket.sendall(str(encrypted_message).encode('utf-8'))

    # Menerima pesan terenkripsi dari server
    data_received = client_socket.recv(1024)
    print("Pesan terenkripsi dari server: ", data_received.decode('utf-8')) ###

    if not data_received:
        print("Koneksi ditutup oleh server.")
        break  # Koneksi ditutup oleh server

    if data_received.decode('utf-8').lower() == "koneksi ditutup oleh server":
        print("Koneksi ditutup oleh server.")
        break  # Koneksi ditutup oleh server

    # Dekripsi pesan
    decrypted_message = int_to_string(encrypt(int(data_received), kunci, True))
    print("<-- Server (Decrypted):", str(decrypted_message))

client_socket.close()
