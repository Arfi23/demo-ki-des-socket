import socket
from des import encrypt, string_to_int, int_to_string

kunci = 0xABCDEF1234567890

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # membuat objek socket, AF-INET : protokol IPv4, SOCK_STREAM : socket tipe stream untuk TCP
server_address = ('localhost', 10235)
server_socket.bind(server_address)
server_socket.listen(1)
print("Server mendengarkan di", server_address)

client_socket, client_address = server_socket.accept() # hasil return berupa objek socket baru (client) dan alamat client
print("Terhubung ke", client_address)

while True:
    # Menerima pesan terenkripsi dari klien
    data_received = client_socket.recv(1024)
    print("Pesan terenkripsi dari client: ", data_received.decode('utf-8')) ###
    if not data_received:
        print("Koneksi ditutup oleh klien.")
        break  # Koneksi ditutup oleh klien

# Jika pesan yang diterima dari client berupa "exit123", koneksi diputus
    if data_received.decode('utf-8').lower() == "koneksi ditutup oleh client":
        print("Koneksi ditutup oleh client.")
        break  # Koneksi ditutup oleh client

    # Dekripsi pesan
    decrypted_message = int_to_string(encrypt(int(data_received), kunci, True))
    print("<-- Client (Decrypted):", str(decrypted_message))

    # Mengetikkan pesan untuk dikirim ke klien
    message_to_send = input("--> Server: ")
    
    # Jika server mengirimkan "exit123", server menutup koneksi
    if message_to_send.lower() == "exit123":
        print("Server meminta penutupan koneksi.")
        message_to_send = "koneksi ditutup oleh server"
        # encrypted_message = encrypt(string_to_int(message_to_send), kunci)
        client_socket.sendall(str(message_to_send).encode('utf-8'))
        break  # Koneksi ditutup oleh server
    
    # Mengirim pesan terenkripsi ke klien
    encrypted_message = encrypt(string_to_int(message_to_send), kunci)
    print("Pesan terenkripsi yang dikirim: ", str(encrypted_message)) #
    client_socket.sendall(str(encrypted_message).encode('utf-8'))

client_socket.close()
server_socket.close()
