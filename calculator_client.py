import tkinter as tk
from tkinter import messagebox
import socket

# Define global variables for the sockets
tcp_socket = None
udp_socket = None
server_address = ('localhost', 9999)

def connect_to_server(protocol):
    global tcp_socket, udp_socket
    # Close any existing connections
    if tcp_socket:
        tcp_socket.close()
        tcp_socket = None
    if udp_socket:
        udp_socket.close()
        udp_socket = None
    # Connect based on the selected protocol
    if protocol == "TCP":
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(server_address)
    elif protocol == "UDP":
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_calculation(protocol, expression):
    try:
        if protocol == "TCP" and tcp_socket:
            tcp_socket.sendall(expression.encode())
            data = tcp_socket.recv(1024).decode()
        elif protocol == "UDP" and udp_socket:
            udp_socket.sendto(expression.encode(), server_address)
            data, _ = udp_socket.recvfrom(1024)
            data = data.decode()
        else:
            raise ConnectionError("No active connection.")
        return data
    except Exception as e:
        messagebox.showerror("Connection error", str(e))
        return ""

def update_expression(char):
    cursor_position = entry_expression.index(tk.INSERT)
    entry_expression.insert(cursor_position, char)

def delete_char():
    cursor_position = entry_expression.index(tk.INSERT)
    entry_expression.delete(cursor_position-1, cursor_position)

def clear_expression():
    entry_expression.delete(0, tk.END)
    entry_result.config(state=tk.NORMAL)
    entry_result.delete(0, tk.END)
    entry_result.config(state=tk.DISABLED)

def set_entry_result(result=""):
    entry_result.config(state=tk.NORMAL)
    entry_result.delete(0, tk.END)
    entry_result.insert(0, result)
    entry_result.config(state=tk.DISABLED)

def calculate():
    expression = entry_expression.get()
    protocol = protocol_var.get()
    if not expression:
        set_entry_result("")
    else:
        try:
            connect_to_server(protocol)  # Ensure we're connected with the correct protocol
            result = send_calculation(protocol, expression)
            set_entry_result(result)
        except Exception as e:
            set_entry_result("")
            messagebox.showerror("Connection error", str(e))
# Create main window
root = tk.Tk()
root.title("Calculator")

# Expression entry
entry_expression = tk.Entry(root, width=40, font=('Arial', 14))
entry_expression.grid(row=0, column=0, columnspan=4)

# Result entry (read-only)
equal_symbol = tk.Label(root, text="=", font=('Arial', 14), padx=10, pady=10)
equal_symbol.grid(row=0, column=4)
entry_result = tk.Entry(root, width=15, state=tk.DISABLED, font=('Arial', 14))
entry_result.grid(row=0, column=5)

# Button setup
buttons = [

    ('(', 1, 0), (')', 1, 1),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1)             , ('+', 5, 3),
]

for (text, row, col) in buttons:
    action = lambda x=text: update_expression(x)
    bg_color = "AntiqueWhite" if text in "0123456789." else "#F0F0F0"
    tk.Button(root, text=text, command=action, width=12, height=5, bg=bg_color).grid(row=row, column=col, pady=5)

tk.Button(root, text='C', command=clear_expression, width=12, height=5).grid(row=1, column=2, pady=5)
tk.Button(root, text='DEL', command=delete_char, width=12, height=5).grid(row=1, column=3, pady=5)
tk.Button(root, text='=', command=calculate, width=12, height=5, bg='aquamarine').grid(row=5, column=2, pady=5)

protocol_text = tk.Label(root, text="Protocol", font=('Arial', 14), padx=10, pady=10)
protocol_text.grid(row=1, column=5, columnspan=2)
protocol_var = tk.StringVar(value="TCP")  # Default value set to TCP
tk.Radiobutton(root, text="TCP", variable=protocol_var, value="TCP", font=('Arial', 16)).grid(row=2, column=5)
tk.Radiobutton(root, text="UDP", variable=protocol_var, value="UDP", font=('Arial', 16)).grid(row=3, column=5)

# Start the main loop
root.mainloop()

# Close sockets when the main loop ends (window is closed)
if tcp_socket:
    tcp_socket.close()
if udp_socket:
    udp_socket.close()