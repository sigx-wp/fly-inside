import socket
import threading
import time

first_tello_address = ("", 8889)
first_local_address = ("", 9010)

first_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
first_socket.bind(first_local_address)


def send(message, delay):
    try:
        first_socket.sendto(message.encode(), first_tello_address)
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

    time.sleep(delay)


def receive():
    while True:
        try:
            first_response, ip_address = first_socket.recvfrom(128)
            print(
                "Received message from Tello #1: "
                + first_response.decode(encoding="utf-8")
            )
        except Exception as exception:
            first_socket.close()
            print("Error receiving: " + str(exception))
            break


received_thread = threading.Thread(target=receive)
received_thread.daemon = True
received_thread.start()

send("command", 3)
send("takeoff", 8)

for i in range(4):
    send("forward 100", 4)
    send("cw 90", 3)

send("land", 5)
print("End!")

first_socket.close()
