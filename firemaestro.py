import socket
import threading

ARM_MESSAGE="arm%s01"
DISARM_MESSAGE="dis%s01"
LAUNCH_MESSAGE="ign%s%02d"
CLEAR_MESSAGE="cls%s%02d"

message_label=None

def start_udp_server(host="0.0.0.0", port=5005):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    thread = threading.Thread(target=udp_receiver, args=(sock,), daemon=True)
    thread.start()
    print("UDP server started in background.")

# --- UDP Receiver (runs in background) ---
def udp_receiver(sock, buffer_size=1024):

    while True:
        data, addr = sock.recvfrom(buffer_size)
        print(f"Received from {addr}: {data.decode(errors='ignore')}")
        message_label.configure(text=f"{data.decode(errors='ignore')}")



def arm(controller):
    send_udp_message(ARM_MESSAGE%controller.port, controller.ip, 4241)

def disarm(controller):
    send_udp_message(DISARM_MESSAGE % controller.port, controller.ip, 4241)

def launch(fw):
    send_udp_message(LAUNCH_MESSAGE%(fw.controller.port, fw.port-1), fw.controller.ip, 4241)

def clear(fw):
    send_udp_message(CLEAR_MESSAGE%(fw.controller.port, fw.port-1), fw.controller.ip, 4241)



# --- UDP Sender ---
def send_udp_message(message, ip="127.0.0.1", port=5005):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 4241))
    sock.sendto(message.encode(), (ip, port))
    sock.close()
    print(f"Sent to {ip}:{port} -> {message}")


def start():
    try:
        start_udp_server("192.168.1.101", 4241)
    except:
        return False
    else:
        return True

