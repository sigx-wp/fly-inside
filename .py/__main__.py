import socket
import threading
import time

first_tello_address = ("", 8889)
second_tello_address = ("", 8889)
third_tello_address = ("", 8889)

first_local_address = ("", 9010)
second_local_address = ("", 9011)
third_local_address = ("", 9012)

first_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
second_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
third_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

first_socket.bind(first_local_address)
second_socket.bind(second_local_address)
third_socket.bind(third_local_address)


def send(message, delay):
    try:
        first_socket.sendto(message.encode(), first_tello_address)
        second_socket.sendto(message.encode(), second_tello_address)
        third_socket.sendto(message.encode(), third_tello_address)
        print("Sending message: " + message)
    except Exception as exception:
        print("Error sending: " + str(exception))

    time.sleep(delay)


def receive():
    while True:
        try:
            first_response, ip_address = first_socket.recvfrom(128)
            second_response, ip_address = second_socket.recvfrom(128)
            print(
                "Received message from Tello #1: "
                + first_response.decode(encoding="utf-8")
            )
            print(
                "Received message from Tello #2: "
                + second_response.decode(encoding="utf-8")
            )
        except Exception as exception:
            first_socket.close()
            second_socket.close()
            print("Error receiving: " + str(exception))
            break


received_thread = threading.Thread(target=receive)
received_thread.daemon = True
received_thread.start()

send("command", 3)
send("takeoff", 8)

send("forward 100", 3)
send("back 100", 3)

send("flip r", 3)
send("flip l", 2)

send("left 90", 3)
send("right 90", 3)

send("flip r", 4)
send("flip l", 3)

send("land", 2)
print("End!")

first_socket.close()
second_socket.close()
