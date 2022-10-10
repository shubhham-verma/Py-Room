import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

bg_color_dark = '#9F8772'
bg_color_light = '#EDE4E0'
button_color = '#C8DBBE'
font_color = "black"
FONT = ("Georgia", 15)
BUTTON_FONT = ("Georgia", 15)
SMALL_FONT = ("Calibri Light", 13)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST, PORT))
        print(f"Successfully connected to server {HOST} on port {PORT}")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages, args=(client,)).start()
    # send_to_server(client)

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


root = tk.Tk()
root.geometry("600x600")
root.title("Py-Room")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=bg_color_dark)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=bg_color_light)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=bg_color_dark)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=bg_color_dark, fg=font_color)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=bg_color_light, fg=font_color, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=button_color, fg=font_color, command=connect)
username_button.pack(fill="none", expand=True, ipadx=10, pady=10)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=bg_color_light, fg=font_color, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=button_color, fg=font_color,command=send_message)
message_button.pack(side=tk.LEFT, padx=10, pady=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=bg_color_light, fg=font_color, width=67,
                                        height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split('~')[0]
            content = message.split('~')[1]

            add_message(f"[{username}] : {content}")

        else:
            print("Message received from client is empty")

def main():

    root.mainloop()



if __name__ == '__main__':
    main()