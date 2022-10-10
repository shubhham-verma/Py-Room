import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
MAX_CLIENTS = 10
current_clients = []

def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            msg = username + '~' + message
            send_to_all(msg)
        else:
            print(f"Message sent from client {username} is empty")


def send_to_client(client, message):
    client.sendall(message.encode())

def send_to_all(message):
    for user in current_clients:
        send_to_client(user[1],message)


def clien_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            current_clients.append((username, client))
            new_user_message = "SERVER~" + f"{username} added to the chat-room"
            send_to_all(new_user_message)
            break
        else:
            print("Please entera valid username")

    threading.Thread(target=listen_for_messages,args=(client, username, )).start()

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} on port {PORT}")
    except:
        print("Unable to connect to the server")

    server.listen(MAX_CLIENTS)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected client to address {address[0]} on port {address[1]}")
        threading.Thread(target=clien_handler, args=(client, )).start()



if __name__ == '__main__':
    main()